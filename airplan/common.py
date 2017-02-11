#---VladVons@gmail.com
# 06.02.17
# micropython ESP8266
#---

import time

cLogSHow = True
#cLogSHow = False


def Log(*aParam):
    if (cLogSHow):
        print("Log: %s" % list(aParam))

def SleepAlways():
    while True:
        # dont burn CPU
        time.sleep_ms(100)

