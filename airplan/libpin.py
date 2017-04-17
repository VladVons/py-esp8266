'''
VladVons@gmail.com
17.04.17
micropython ESP8266
'''

import machine


def SetPin(aPin, aValue):
    #log.Log(3, 'SetPin', 'Pin', aPin, 'Value', aValue)
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
    #log.Log(3, 'SetPwmFreq', 'Pin', aPin, 'Value', aValue)
    Obj = machine.PWM(machine.Pin(aPin))
    Obj.freq(aValue)
    return Obj.freq()

def SetPwmDuty(aPin, aValue):
    #log.Log(3, 'SetPwmDuty', 'Pin', aPin, 'Value', aValue)
    Obj = machine.PWM(machine.Pin(aPin))
    Obj.duty(aValue)
    return Obj.duty()

def SetPwmOff(aPin):
    #log.Log(3, 'SetPwmOff', 'Pin', aPin)
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

def GetAdc(aPin):
    Obj = machine.ADC(aPin)
    return Obj.read()

def SetButton(aPin, aHandler):
    #http://docs.micropython.org/en/v1.8.6/wipy/library/machine.Pin.html
    Obj = machine.Pin(aPin, machine.Pin.IN)
    Obj.irq(trigger = machine.Pin.IRQ_FALLING, handler = aHandler)

