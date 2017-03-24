#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---

import machine
import gc
#
import wlan
import fs


cPinLedRed   = 15
cPinLedGreen = 12
cPinLedBlue  = 13
cPinLedSys   = 02
#
cPinBtnFlush = 0
cPinBtnPush  = 4


def FileLoad(aName):
    return fs.FileLoad(aName)

def FileList():
    return '\n'.join(fs.FileList())

def SetEssd(aName, aPassw):
    wlan.SetEssd('vando-' + aName, aPassw)

def SetButton(aPin, aHandler):
    Obj = machine.Pin(aPin, machine.Pin.IN)
    Obj.irq(trigger = machine.Pin.IRQ_FALLING, handler = aHandler)

def SetPin(aPin, aOn):
    Obj = machine.Pin(aPin, machine.Pin.OUT)
    Obj.value(aOn)
    return Obj.value()

def GetPin(aPin):
    try:
        Obj = machine.Pin(aPin, machine.Pin.OUT)
        Result = Obj.value()
    except:
        Result = -1
    return Result

def SetPins(aPins, aOn):
    for Pin in aPins:
        SetPin(Pin, aOn)
    return None

def SetPwm(aPin, aFreq, aDuty):
    Obj = machine.PWM(machine.Pin(aPin))
    Obj.freq(aFreq)
    Obj.duty(aDuty)
    return (Obj.freq(), Obj.duty())

def GetPwm(aPin):
    try:
        Obj = machine.PWM(machine.Pin(aPin))
        Result = (Obj.freq(), Obj.duty())
    except:
        Result = (-1, -1)        
    return Result

def StopPwm(aPin):
    Obj = machine.PWM(machine.Pin(aPin))
    Obj.deinit()
    return 0

def GetAdc():
    Obj = machine.ADC(0)
    return Obj.read()

def GetMemFree():
    gc.collect()
    return gc.mem_free()

def Reset():
    machine.reset()
