#---VladVons@gmail.com
# 08.04.17
# micropython ESP8266
#---

import api

class TTimer:
    def __init__(self, aTimeOut = 1000, aHandler = None):
        self.TimeOut    = aTimeOut
        self.Handler    = aHandler
        self.LastUpdate = api.GetTicks()
        self.LastTag    = api.GetTicks()
        self.Tag        = 0
        self.CntCheck   = 0
    
    def Check(self):
        return api.GetTicks() - self.LastUpdate > self.TimeOut
   
    def Update(self):
        self.LastUpdate = api.GetTicks()

    def Handle(self):
        Result = None
        if self.Check():
            self.Update()
            self.CntCheck += 1 
            if (self.Handler):
                Result = self.Handler()
        return Result

    def IncTag(self, aInc = 1, aTimeOut = 250):
        Ticks = api.GetTicks()
        Dif   = Ticks - self.LastTag
        if (Dif > aTimeOut):
            self.Tag += aInc
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
