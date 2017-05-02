#---VladVons@gmail.com
# 17.04.17
# micropython ESP8266
#---

import machine
import time


def GetTicks():
    return time.ticks_ms()

def Sleep(aDelay):
    time.sleep_ms(aDelay)

def TimerCallback(aTimeOut, aHandler):
    obj = machine.Timer(-1)
    obj.init(period = aTimeOut, mode = machine.Timer.PERIODIC, callback = aHandler)
    
class TTimer:
    def __init__(self, aHandler, aTimeOut = 1000):
        self.TimeOut    = aTimeOut
        self.Handler    = aHandler
        self.LastUpdate = GetTicks()
        self.CntTimeOut = 0

    def IsTimeOut(self):
        return GetTicks() - self.LastUpdate > self.TimeOut

    def Update(self):
        self.LastUpdate = GetTicks()

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
        self.LastTag  = GetTicks()
        self.CntTag   = 0
        self.Debounce = aDebounce

    def IncTag(self):
        Ticks = GetTicks()
        Dif   = Ticks - self.LastTag
        if (Dif > self.Debounce):
            self.CntTag += 1
        self.LastTag = Ticks

#def WatchDog(aTimeOut = 0):
#    obj = machine.WDT()
#    obj.feed()

