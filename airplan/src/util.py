#---VladVons@gmail.com
# 05.04.17
# micropython ESP8266
#---


def SpeedTest(aCount, aPin):
    import speedtest
    return speedtest.TestAll(aCount, aPin)

