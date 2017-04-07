#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---

import api
from app import TApp
#import ntptime

def Main():
    #https://github.com/micropython/micropython/blob/master/esp8266/scripts/ntptime.py
    #ntptime.settime()
 
    App = TApp()
    print("GetInfo", api.GetInfo())
    print("Mem free", api.GetMemFree(), "Ticks", api.GetTicks())
    print("Mac", api.GetMac(), "ID")
    App.Listen()


Main()

#import os, sys
#print('uname', os.uname())
#print('version', sys.version())
