#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---

import time
import machine
#
from common import Log
from control import TPinOut

class TLeds:
    def __init__(self):
        Log('TLeds.init');

        self.Idx  = 0

        self.Leds = []
        self.Leds.append(TPinOut(2,  "sys"))
        self.Leds.append(TPinOut(15, "red"))
        self.Leds.append(TPinOut(12, "green"))
        self.Leds.append(TPinOut(13, "blue"))

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
