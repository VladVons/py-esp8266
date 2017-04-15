#---VladVons@gmail.com
# 08.04.17
# micropython ESP8266
#---

import os
import ustruct
import ubinascii
import uhashlib
#
import api
import wlan


def GetRand(aMin = 0, aMax = 65536):
    Rand = ustruct.unpack("I", os.urandom(4))[0]
    return aMin + (Rand % (aMax - aMin))

def GetSerial():
    Bytes = uhashlib.sha256(wlan.GetMac()).digest()
    Hash  = ubinascii.hexlify(Bytes).decode('utf-8')
    return "%s-%s-%s-%s" % (Hash[8:12], Hash[16:20], Hash[24:28], Hash[32:36])

class TTimer:
    def __init__(self, aHandler, aTimeOut = 1000):
        self.TimeOut    = aTimeOut
        self.Handler    = aHandler
        self.LastUpdate = api.GetTicks()
        self.CntTimeOut = 0
    
    def IsTimeOut(self):
        return api.GetTicks() - self.LastUpdate > self.TimeOut
   
    def Update(self):
        self.LastUpdate = api.GetTicks()

    def Handle(self):
        Result = None
        if (self.IsTimeOut()):
            self.Update()
            self.CntTimeOut += 1 
            if (self.Handler):
                Result = self.Handler()
        return Result


class TTimerDebounce(TTimer):
    def __init__(self, aHandler, aTimeOut = 1000, aDebounce = 200):
        TTimer.__init__(self, aHandler, aTimeOut)
        self.LastTag  = api.GetTicks()
        self.CntTag   = 0
        self.Debounce = aDebounce

    def IncTag(self):
        Ticks = api.GetTicks()
        Dif   = Ticks - self.LastTag
        if (Dif > self.Debounce):
            self.CntTag += 1
        self.LastTag = Ticks



'''
def DebouncePin(aObj):
    CurVal = aObj.value()
    Active = 0
    while (Active < 20):
        if (aObj.value() != CurVal):
            Active += 1
        else:
            Active = 0
        api.Sleep(1)
'''
