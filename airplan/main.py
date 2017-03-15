#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---

import api
from app import TApp

def Main():
    App = TApp()
    print("Mem free", api.GetMemFree())
    App.Listen()


Main()
