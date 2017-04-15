#---VladVons@gmail.com
# 05.02.17
# micropython ESP8266
#---

import network
import time
import ubinascii


def Scan():
    Result = []

    Obj = network.WLAN(network.STA_IF)
    nets = Obj.scan()
    for net in nets:
        Result.append(net[0].decode('utf-8'))

    return Result

def GetMacByte():
    Obj = network.WLAN(network.AP_IF)
    return Obj.config("mac")

def GetMac():
    Mac = ubinascii.hexlify(GetMacByte()).decode('utf-8')
    return ':'.join(Mac[i : i+2] for i in range(0, 12, 2))

def SetEssId(aName, aPassw):
    essid = '%s-%s' % (aName, GetMac()[-4:])
    Obj = network.WLAN(network.AP_IF)
    return Obj.config(essid = essid, authmode = network.AUTH_WPA_WPA2_PSK, password = aPassw)

def GetInfo():
    Obj = network.WLAN(network.STA_IF)
    return Obj.ifconfig()

def Connect(aESSID, aPassw, aTimeOut = 10000):
    Obj = network.WLAN(network.STA_IF)
    Result = Obj.isconnected()
    if (not Result):
        Obj.active(True)
        Obj.connect(aESSID, aPassw)

        TimeEnd = time.ticks_ms() + aTimeOut
        while (True):
            #machine.idle()
            time.sleep_ms(250)

            Result = Obj.isconnected()
            if (Result or time.ticks_ms() > TimeEnd):
                break

    return Result
