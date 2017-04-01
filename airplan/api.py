'''
VladVons@gmail.com
04.02.17
micropython ESP8266
'''

import machine
import gc
import time
import os
##
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
    return {"Version":  "1.04", 
            "Date":     "2017.04.01", 
            "Support" : "VladVons@gmail.com"}

def Exec(aValue = "Result = (2+3)*2"):
    Result = None
    Vars   = {}
    try:
        exec(aValue, globals(), Vars)
        Result = Vars.get('Result')
    except Exception as E:
        print(E)
        Result = E
    return Result

def Print(aValue = ""):
    print(aValue)

def FileLoad(aName):
    return fs.FileLoad(aName)

def FileList():
    return '\n'.join(fs.FileList())

def SetEssd(aName, aPassw):
    wlan.SetEssd('vando-' + aName, aPassw)

def GetMac():
    return wlan.GetMac()

def GetMemFree():
    gc.collect()
    return gc.mem_free()

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
    Obj = machine.Pin(aPin, machine.Pin.IN)
    Obj.irq(trigger = machine.Pin.IRQ_FALLING, handler = aHandler)

def Reset():
    machine.reset()

#--- Pin support

def SetPin(aPin, aOn):
    Obj = machine.Pin(aPin, machine.Pin.OUT)
    Obj.value(aOn)
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
    Obj = machine.PWM(machine.Pin(aPin))
    Obj.freq(aValue)
    return Obj.freq()

def SetPwmDuty(aPin, aValue):
    Obj = machine.PWM(machine.Pin(aPin))
    Obj.duty(aValue)
    return Obj.duty()

def SetPwmOff(aPin):
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

#--- Pin array support

def CallArr(aFunc, aItems, aArgs = []):
    Result = []
    for Item in aItems:
        ArgCnt = len(aArgs)
        if (ArgCnt == 1):
            Result.append(aFunc(Item, aArgs[0]))
        elif (ArgCnt == 2):
            Result.append(aFunc(Item, aArgs[0], aArgs[1]))
        else:
            Result.append(aFunc(Item))
    return Result

def GetPinArr(aPins):
    return CallArr(GetPin, aPins)

def GetPwmDutyArr(aPins):
    return CallArr(GetPwmDuty, aPins)

def GetPwmFreqArr(aPins):
    return CallArr(GetPwmFreq, aPins)

def SetPinInvArr(aPins):
    return CallArr(SetPinInv, aPins)

def SetPwmOffArr(aPins):
    return CallArr(SetPwmOff, aPins)


def SetPinArr(aPins, aValue):
    return CallArr(SetPin, aPins, [aValue])

def SetPwmFreqArr(aPins, aValue):
    return CallArr(SetPwmFreq, aPins, [aValue])

def SetPwmDutyArr(aPins, aValue):
    return CallArr(SetPwmDuty, aPins, [aValue])
