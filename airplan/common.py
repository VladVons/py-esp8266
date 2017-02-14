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

def SleepAlways():
    while True:
        # dont burn CPU
        time.sleep_ms(100)

#---
class TFile():
    @staticmethod
    def List():
        return uos.listdir()

    @staticmethod
    def Exists(aFile):
        Files = TFile.List()
        return (aFile in Files)

    @staticmethod
    def Load(aName):
        File = open(aName)
        Result = File.read()
        File.close()
        return Result
 