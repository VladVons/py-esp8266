'''
VladVons@gmail.com
04.02.17
micropython ESP8266
'''

import sys
import machine
#
import log
import wlan
import lib
import libpin
import libtime
import fs

def GetInfo():
    return {
            "Software": "1.0.13",
            "Date":     "2017.04.17",
            "Hardware": "1.1.2",
            "Author":   "Volodymyr Vons",
            "EMail":    "VladVons@gmail.com",
            "Homepage": "http://vando.com.ua/esp",
            "Platform": sys.platform,
            "Python":   sys.version,
            "MacAddr":  wlan.GetMac(),
            "MemFree":  lib.GetMemFree(),
            "MemAlloc": lib.GetMemAlloc(),
            "Freq MHz": int(machine.freq() / 1000000),
            "Uptime":   int(libtime.GetTicks() / 1000),
            "Firmware": "%d.%d.%d" % sys.implementation[1]
           }

def Exec(aValue):
    return lib.Exec(aValue)


# --- File
def FileRead(aName):
    return fs.FileRead(aName)

def FileWrite(aName, aData):
    return fs.FileWrite(aName, aData)

def FileList():
    return '\n'.join(fs.FileList())


# --- Log
def Log(aLevel, aValue = ''):
    log.Log(aLevel, aValue)

def SetLogLevel(aValue):
    log.LogLevel = aValue


#--- Net
def SetEssd(aName, aPassw):
    wlan.SetEssId('vando-' + aName, aPassw)

def GetMac():
    return wlan.GetMac()

def WlanSTA(aEssId, aPassw):
    return wlan.Connect(aEssId, aPassw)


# --- Timer
def Sleep(aDelay):
    libtime.Sleep(aDelay)

def GetTicks():
    return libtime.GetTicks()


# --- CPU
def Reset():
    return lib.Reset()

def CpuBurst(aValue):
    return lib.CpuBurst(aValue)


# --- Mass caller
def CallObjArr(*aArgs):
    Result = []
    Obj = aArgs[0]
    for i in range(1, len(aArgs)):
        Result.append(Obj(*aArgs[i]))
    return Result

def CallFuncArr(*aArgs):
    Args = list(aArgs)
    Args[0] = eval(Args[0])
    return CallObjArr(*Args)


# --- Pin
def SetPin(aPin, aValue):
    return libpin.SetPin(aPin, aValue)

def SetPinInv(aPin):
    return libpin.SetPinInv(aPin)

def GetPin(aPin):
    return libpin.GetPin(aPin)

def SetPwmFreq(aPin, aValue):
    return libpin.SetPwmFreq(aPin, aValue)

def SetPwmDuty(aPin, aValue):
    return libpin.SetPwmDuty(aPin, aValue)

def SetPwmOff(aPin):
    return libpin.SetPwmOff(aPin)

def GetPwmDuty(aPin):
    return libpin.GetPwmDuty(aPin)

def GetPwmFreq(aPin):
    return libpin.GetPwmFreq(aPin)

def GetAdc(aPin = 0):
    return libpin.GetAdc(aPin)

