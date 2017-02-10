#---VladVons@gmail.com
# 06.02.17
# micropython ESP8266
#---

cLogSHow = True
#cLogSHow = False


def Log(*aParam):
    if (cLogSHow):
        print("Log: %s" % list(aParam))
