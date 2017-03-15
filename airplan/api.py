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
cPinLedSys   = 2
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

def SetLed(aPin, aOn):
    Obj = machine.Pin(aPin, machine.Pin.OUT)
    Obj.value(aOn)
    return Obj.value()

def GetLed(aPin):
    Obj = machine.Pin(aPin, machine.Pin.OUT)
    return Obj.value()

def SetPwm(aPin, aFreq, aDuty):
    Obj = machine.PWM(machine.Pin(aPin))
    Obj.freq(aFreq)
    Obj.duty(aDuty)
    return (Obj.freq(), Obj.duty())

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
