#---VladVons@gmail.com
# 06.02.17
# micropython ESP8266
#---

import machine
import time
#
from common import Log


class TPinBase:
    def __init__(self, aPin, aAlias):
        Log('TPinBase.init', aPin, aAlias);
        self.Pin   = aPin
        self.Alias = aAlias


class TPinOut(TPinBase):
    def __init__(self, aPin, aAlias = ''):
        TPinBase.__init__(self, aPin, aAlias)
        self.Obj = machine.Pin(aPin, machine.Pin.OUT)

    def Set(self, aOn):
        Log('TPinOut.Set', aOn, self.Alias, self.Pin)
        self.Obj.value(aOn)

    def Get(self):
        return self.Obj.value()

    def Toggle(self):
        Log("TPinOut.Toggle")
        self.Set(not self.Get())

    def Flash(self, aCount = 1, aDelay = 100):
        Log("TPinOut.Flash", aCount, aDelay)
        for i in range(0, aCount):
            self.Set(True)
            time.sleep_ms(aDelay)
            self.Set(False)
            time.sleep_ms(aDelay)


class TPinIn(TPinBase):
    def __init__(self, aPin, aHandler, aAlias = ''):
        TPinBase.__init__(self, aPin, aAlias)

        self.Obj = machine.Pin(aPin, machine.Pin.IN)
        self.Obj.irq(trigger = machine.Pin.IRQ_FALLING, handler = aHandler)


class TTimer():
    def __init__(self, aNum, aHandler, aPeriod = 1000):
        self.Timer = machine.Timer(-1)
        self.Timer.init(period=aPeriod, mode = machine.Timer.PERIODIC, callback = aHandler)


