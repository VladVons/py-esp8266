#---VladVons@gmail.com
# 08.04.17
# micropython ESP8266
#---

import os
import ustruct
#
import api

def GetRand(aMax = 256):
    return ustruct.unpack("I", os.urandom(4))[0] % aMax

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
