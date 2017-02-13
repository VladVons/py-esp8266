#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---

from net import *
#from app import TApp

def Main():
    time.sleep_ms(1000)

    gc.collect()
    print("Mem free a1", gc.mem_free())
    #print(dir(machine))

    #App = TApp()
    #App.TestLeds(1*4)
    #App.TestSpeed(1000)
    #App.Listen()

    WLan = TWLan()
    WLan.Connect('R3-0976646510', '19710000')

    ServerRun('0.0.0.0', 80)

Main()
