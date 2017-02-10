#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---

import time
import machine
from common import *

#------------------------------------------
class TLed:
    def __init__(self, aPin, aAlias = ''):
        Log('TLed.init', aPin, aAlias);

        self.Pin   = aPin
        self.Alias = aAlias
        self.Obj   = machine.Pin(aPin, machine.Pin.OUT)

    def Set(self, aOn):
        Log("TLed.Set", aOn, self.Alias, self.Pin)

        self.Obj.value(aOn)

    def Get(self):
        return self.Obj.value()

    def Toggle(self):
        Log("TLed.Toggle")

        self.Set(not self.Get())

    def Flash(self, aCount = 1, aDelay = 100):
        Log("TLed.Flash", aCount, aDelay)

        for i in range(0, aCount):
            self.Set(True)
            time.sleep_ms(aDelay)
            self.Set(False)
            time.sleep_ms(aDelay)


#------------------------------------------
class TLeds:
    def __init__(self):
        Log('TLeds.init');

        self.Idx  = 0

        self.Leds = []
        self.Leds.append(TLed(2,  "sys"))
        self.Leds.append(TLed(15, "red"))
        self.Leds.append(TLed(12, "green"))
        self.Leds.append(TLed(13, "blue"))

    def GetCount(self):
        return len(self.Leds)

    def GetIdx(self, aName):
        for i in range(len(self.Leds)):
            if (self.Leds[i].Alias == aName):
                return i
        return -1

    def GetObj(self, aName):
        for Led in self.Leds:
            if (Led.Alias == aName):
                return Led
        return None

    def Toggle(self):
        Log("TLeds.Toggle")

        Led = self.Leds[self.Idx]
        Led.Flash(1)

        self.Idx += 1
        if (self.Idx >= self.GetCount()):
            self.Idx = 0 

    def SetNo(self, aIdx, aOn):
        Log('TLeds.SetNo', aIdx, aOn);

        if (aIdx < len(self.Leds)):
            self.Leds[aIdx].Set(aOn)
        else:
            print('index out of range', aIdx)

    def Set(self, aOn):
        Log('TLeds.Set-2', aOn);

        # here is error: MemoryError
        for Led in self.Leds:
        #for i in range(len(self.Leds)):
            #Led = self.Leds[i]
            Led.Set(aOn)
