#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---

import log
import app
import config
import wlan


def GetConfig():
    Config = config.TConfig()
    Config.FileLoad('config.json')
    return Config.GetItems()

def WlanSTA(aConf):
    if (aConf.get('/STA/Enable', False)):
        ESSID  = aConf.get('/STA/ESSID', '')
        Paswd  = aConf.get('/STA/Password', '')
        log.Log(1, 'WlanSTA()', ESSID, Paswd)
        if (wlan.Connect(ESSID,  Paswd)):
            log.Log(1, 'Network', wlan.GetInfo())

def WlanAP(aConf):
    if (aConf.get('/AP/Enable', False)):
        ESSID  = aConf.get('/AP/ESSID', 'micropythoN')
        Paswd  = aConf.get('/AP/Password', 'micropythoN')
        wlan.SetEssId(ESSID, Paswd)
        log.Log(1, 'WlanAP()', ESSID, Paswd)
    else:
        log.Log(1, 'AP Password: micropythoN')

def Main(): 
    #https://github.com/micropython/micropython/blob/master/esp8266/scripts/ntptime.py
    #import ntptime
    #ntptime.settime()

    Config = GetConfig()
    WlanAP(Config)
    WlanSTA(Config)

    App = app.TApp(Config)
    App.Listen()

Main()
