#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---

import gc
from app import TApp

def Main():
    App = TApp()
    #App.TestLeds(1*4)
    print("Mem free", gc.mem_free())
    App.Listen()


Main()
