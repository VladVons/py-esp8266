#---VladVons@gmail.com
# 01.02.17
# micropython ESP8266
#---

LogLevel = 1

def Log(aLevel, *aParam):
    if (aLevel <= LogLevel):
        print('Level %d: %s%s' % (aLevel, ' ' * aLevel, list(aParam)))
