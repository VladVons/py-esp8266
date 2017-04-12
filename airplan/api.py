'''
VladVons@gmail.com
04.02.17
micropython ESP8266
'''

import machine
import gc
import time
import os
import sys
##
import log
import wlan
import fs

cPinLedRed   = 15
cPinLedGreen = 12
cPinLedBlue  = 13
cPinLedSys   = 02
#
cPinBtnFlush = 0
cPinBtnPush  = 4
#
#ArrPwm    = [0, 2, 4, 5, 12, 13, 14, 15]
#ArrPin    = [0, 1, 2, 3, 4, 5, 12, 13, 14, 15, 16]
ArrLed    = [cPinLedSys, cPinLedRed, cPinLedGreen, cPinLedBlue]
ArrMotor1 = [13, 12]
ArrMotor2 = [14, 15]


def GetInfo():
    return {
            "Software": "1.0.9", 
            "Date":     "2017.04.12", 
            "Hardware": "1.1.2", 
            "Author":   "Volodymyr Vons",
            "Support":  "http://vando.com.ua/esp",
            "Platform": sys.platform,
            "Python":   sys.version,
            "MacAddr":  GetMac(),
            "MemFree":  GetMemFree(),
            "MemAlloc": GetMemAlloc(),
            "Freq MHz": int(machine.freq() / 1000000),
            "Uptime":   int(GetTicks() / 1000),
            "Firmware": "%d.%d.%d" % sys.implementation[1]
           }

def Exec(aValue = 'Result = (2+3)*2'):
    Result = None
    Vars   = {}
    try:
        exec(aValue, globals(), Vars)
        Result = Vars.get('Result')
    except Exception as e:
        print(e)
        Result = e
    return Result

def Print(aValue = ''):
    print(aValue)

def Log(aLevel, aValue = ''):
    log.Log(aLevel, aValue)

def Dump(aValue, aPref = ''):
    if (isinstance(aValue, dict)):
        for Key in aValue:
            Dump(aValue[Key], aPref + '/' + Key)
    elif (isinstance(aValue, list)):
        for Value in aValue:
            Dump(Value, aPref)
    else:
        print(aPref, aValue)

def SetLogLevel(aValue):
    log.LogLevel = aValue

def FileRead(aName):
    return fs.FileRead(aName)

def FileWrite(aName, aData):
    return fs.FileWrite(aName, aData)

def FileList():
    return '\n'.join(fs.FileList())

def SetEssd(aName, aPassw):
    wlan.SetEssId('vando-' + aName, aPassw)

def GetMac():
    return wlan.GetMac()

def ConnectWlan(aEssId, aPassw):
    return wlan.Connect(aEssId, aPassw)

def GetMemFree():
    gc.collect()
    return gc.mem_free()

def GetMemAlloc():
    gc.collect()
    return gc.mem_alloc()

def Sleep(aDelay):
    time.sleep_ms(aDelay)

def GetTicks():
    return time.ticks_ms()

#def GetMachineId():
#    return machine.unique_id().decode("utf-8")

#def WatchDog(aTimeOut = 0):
#    obj = machine.WDT()
#    obj.feed()

def TimerCallback(aTimeOut, aHandler):
    obj = machine.Timer(-1)
    obj.init(period = aTimeOut, mode = machine.Timer.PERIODIC, callback = aHandler)

def SetButton(aPin, aHandler):
    #http://docs.micropython.org/en/v1.8.6/wipy/library/machine.Pin.html
    Obj = machine.Pin(aPin, machine.Pin.IN)
    Obj.irq(trigger = machine.Pin.IRQ_FALLING, handler = aHandler)

def Reset():
    machine.reset()

#--- Pin support

def SetPin(aPin, aValue):
    log.Log(3, 'SetPin', 'Pin', aPin, 'Value', aValue)

    Obj = machine.Pin(aPin, machine.Pin.OUT)
    Obj.value(aValue)
    return Obj.value()

def SetPinInv(aPin):
    Obj = machine.Pin(aPin, machine.Pin.OUT)
    Obj.value(not Obj.value())
    return Obj.value()

def GetPin(aPin):
    try:
        Obj = machine.Pin(aPin, machine.Pin.OUT)
        Result = Obj.value()
    except:
        Result = -1
    return Result

def SetPwmFreq(aPin, aValue):
    log.Log(3, 'SetPwmFreq', 'Pin', aPin, 'Value', aValue)

    Obj = machine.PWM(machine.Pin(aPin))
    Obj.freq(aValue)
    return Obj.freq()

def SetPwmDuty(aPin, aValue):
    log.Log(3, 'SetPwmDuty', 'Pin', aPin, 'Value', aValue)

    Obj = machine.PWM(machine.Pin(aPin))
    Obj.duty(aValue)
    return Obj.duty()

def SetPwmOff(aPin):
    log.Log(3, 'SetPwmOff', 'Pin', aPin)

    Obj = machine.PWM(machine.Pin(aPin))
    Obj.deinit()
    return None

def GetPwmDuty(aPin):
    try:
        Obj = machine.PWM(machine.Pin(aPin))
        Result = (Obj.duty())
    except:
        Result = -1
    return Result

def GetPwmFreq(aPin):
    try:
        Obj = machine.PWM(machine.Pin(aPin))
        Result = (Obj.freq())
    except:
        Result = -1
    return Result

def GetAdc(aPin = 0):
    Obj = machine.ADC(aPin)
    return Obj.read()

#--- pin array function
def SetPinArr(aPins, aValue):
    Result = []    
    for Pin in aPins:
        Result.append(SetPin(Pin, aValue))    
    return Result

def SetPwmOffArr(aPins):
    Result = []    
    for Pin in aPins:
        Result.append(SetPwmOff(Pin))    
    return Result
