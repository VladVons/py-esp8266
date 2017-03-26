#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---

import api
from app import TApp

def Main():
    print("Version", api.GetInfo(), "Mem free", api.GetMemFree(), "Ticks", api.GetTicks(), "ID", api.GetMachineId())

    App = TApp()
    App.Listen()


Main()

#import os, sys
#print('uname', os.uname())
#print('version', sys.version())
