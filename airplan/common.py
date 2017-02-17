#---VladVons@gmail.com
# 06.02.17
# micropython ESP8266
#---

import time
import uos

cLogSHow = True

def Log(*aParam):
    if (cLogSHow):
        print("Log: %s" % list(aParam))

'''
def SleepAlways():
    while True:
        # dont burn CPU
        time.sleep_ms(100)

def TestSpeed(self, aCount):
    import ujson
    import time

    TimeStart = time.ticks_ms()
    for i in range(aCount):
        #DataIn  = ujson.dumps( {'data': i} )
        #DataOut = ujson.loads(DataIn)
        Val = int(i % 2)
        self.Leds.Set(Val)

    print('MSec', time.ticks_ms() - TimeStart)
'''
