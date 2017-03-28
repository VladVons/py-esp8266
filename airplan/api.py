#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---

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
#ArrLed    = [cPinLedSys, cPinLedRed, cPinLedGreen, cPinLedBlue]
#ArrMotor1 = [13, 12]
#ArrMotor2 = [14, 16]


def GetInfo():
    return {"Version":  "1.02", 
            "Date":     "2017.03.28", 
            "Support" : "VladVons@gmail.com"}

def Exec(aValue = "Result = (2+3)*2"):
    Vars = {}
    try:
        exec(aValue, globals(), Vars)
        Result = Vars.get('Result')
    except Exception as E:
        print(E)
        Result = E
    return Result

def Print(aValue):
    print(aValue)

def FileLoad(aName):
    return fs.FileLoad(aName)

def FileList():
    return '\n'.join(fs.FileList())

def SetEssd(aName, aPassw):
    wlan.SetEssd('vando-' + aName, aPassw)

def GetMemFree():
    gc.collect()
    return gc.mem_free()

def Sleep(aDelay):
    time.sleep_ms(aDelay)

def GetTicks():
    return time.ticks_ms()

def GetMachineId():
    return machine.unique_id()

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

def GetPwm(aPin):
    try:
        Obj = machine.PWM(machine.Pin(aPin))
        Result = (Obj.freq(), Obj.duty())
    except:
        Result = (-1, -1)
    return Result

def GetAdc(aPin = 0):
    Obj = machine.ADC(aPin)
    return Obj.read()

#--- Pin array support

def GetPins(aPins):
    Result = []
    for Pin in aPins:
        Result.append(GetPin(Pin))
    return Result

def SetPins(aPins, aOn):
    Result = []
    for Pin in aPins:
        Result.append(SetPin(Pin, aOn))
    return Result

def SetPinsInv(aPins):
    Result = []
    for Pin in aPins:
        Result.append(SetPinInv(Pin))
    return Result

def GetPwms(aPins):
    Result = []
    for Pin in aPins:
        Result.append(GetPwm(Pin))
    return Result

def SetPwmsOff(aPins):
    for Pin in aPins:
        SetPwmOff(Pin)
    return None
