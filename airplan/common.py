#---VladVons@gmail.com
# 08.04.17
# micropython ESP8266
#---

import api

class TTimer:
    def __init__(self, aTimeOut = 1000, aHandler = None):
        self.TimeOut = aTimeOut
        self.Handler = aHandler
        self.Cnt     = 0
        self.Update()
    
    def Check(self):
        return api.GetTicks() - self.Last > self.TimeOut
   
    def Update(self):
        self.Last = api.GetTicks()

    def Handle(self):
        Result = None
        if self.Check():
            self.Update()
            self.Cnt += 1 
            if (self.Handler):
                Result = self.Handler()
        return Result
