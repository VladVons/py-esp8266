#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---

import api
import config
import app

def GetConfig():
    Config = config.TConfig()
    Config.FileLoad('config.json')
    return Config.GetItems()
   
def Main():
    #https://github.com/micropython/micropython/blob/master/esp8266/scripts/ntptime.py
    #import ntptime
    #ntptime.settime()
 
    App = app.TApp(GetConfig())
    api.Dump(api.GetInfo())
    App.ConnectWlan()
    App.Listen()

Main()

#import os, sys
#print('uname', os.uname())
