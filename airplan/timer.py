#---VladVons@gmail.com
# 06.02.17
# micropython. ESP8266
#---


import machine

class TTimer():
    def __init__(self, aNum, aCallBack, aPeriod = 1000):
        self.Timer = machine.Timer(-1)
        self.Timer.init(period=aPeriod, mode = machine.Timer.PERIODIC, callback = aCallBack)
