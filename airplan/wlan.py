#---VladVons@gmail.com
# 05.02.17
# micropython ESP8266
#---

import network
import time
import ubinascii
#
#from common import Log

def Scan():
    Result = []

    wlan = network.WLAN(network.STA_IF)
    nets = wlan.scan()
    for net in nets:
        Result.append(net[0].decode("utf-8"))

    return Result

def GetMac():
    ap_if = network.WLAN(network.AP_IF)
    mac = ap_if.config("mac")
    return ubinascii.hexlify(mac).decode("utf-8")

def SetEssd(aName, aPassw):
    essid = "%s-%s" % (aName, GetMac()[-4:])
    ap_if = network.WLAN(network.AP_IF)
    ap_if.config(essid = essid, authmode = network.AUTH_WPA_WPA2_PSK, password = aPassw)

def GetInfo():
    wlan = network.WLAN(network.STA_IF)
    return wlan.ifconfig()

def Connect(aESSID, aPassw, aTimeOut = 10000):
    wlan = network.WLAN(network.STA_IF)
    Result = wlan.isconnected()
    if (not Result):
        wlan.active(True)
        wlan.connect(aESSID, aPassw)

        TimeEnd = time.ticks_ms() + aTimeOut
        while (True):
            #machine.idle()
            time.sleep_ms(250)

            Result = wlan.isconnected()
            if (Result or time.ticks_ms() > TimeEnd):
                break

    return Result

