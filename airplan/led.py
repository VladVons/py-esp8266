#---VladVons@gmail.com
# 04.02.17
#---

import time
import machine


#------------------------------------------
class TLed:
    def __init__(self, aPin, aAlias = ''):
        print('TLed.init', aPin, aAlias);

        self.Pin   = aPin
        self.Alias = aAlias
        self.Obj   = machine.Pin(aPin, machine.Pin.OUT)

    def Set(self, aOn):
        print("TLed.Set", aOn, self.Alias, self.Pin)

        self.Obj.value(aOn)

    def Get(self):
        return self.Obj.value()

    def Toggle(self):
        print("TLed.Toggle")

        self.Set(not self.Get())

    def Flash(self, aCount = 1, aDelay = 100):
        print("TLed.Flash", aCount, aDelay)

        for i in range(0, aCount):
            self.Set(True)
            time.sleep_ms(aDelay)
            self.Set(False)
            time.sleep_ms(aDelay)


#------------------------------------------
class TLeds:
    def __init__(self):
        print('TLeds.init');

        self.Idx  = 0

        self.Leds = []
        self.Leds.append(TLed(2,  "Sys"))
        self.Leds.append(TLed(15, "Red"))
        self.Leds.append(TLed(12, "Green"))
        self.Leds.append(TLed(13, "Blue"))

    def GetCount(self):
        return len(self.Leds)

    def Toggle(self):
        print("TLeds.Toggle")
 
        Led = self.Leds[self.Idx]
        Led.Flash(1)

        self.Idx += 1
        if (self.Idx >= self.GetCount()):
            self.Idx = 0 

    def SetNo(self, aIdx, aOn):
        print('TLeds.SetNo', aIdx, aOn);

        if (aIdx < len(self.Leds)):
            self.Leds[aIdx].Set(aOn)
        else:
            print('index out of range', aIdx)

    def Set(self, aOn):
        print('TLeds.Set-2', aOn);

        # here is error: MemoryError
        for Led in self.Leds:
        #for i in range(len(self.Leds)):
            #Led = self.Leds[i]
            Led.Set(aOn)
