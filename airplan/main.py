#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---

from net import *
from app import TApp

def Main():
    time.sleep_ms(3000)

    #gc.collect()
    #print("Mem free", gc.mem_free(), "Mac", TWLan.GetMac())
    #print(dir(machine))

    App = TApp()
    App.TestLeds(1*4)
    #App.TestSpeed(1000)
    App.Listen()

    #TWLan.SetEssd('PinkFloyd', '19790000')
    #Con = TWLan.Connect('R3-0976646510', '19710000')
    #if (Con):
    #    print('Network', TWLan.GetInfo())
    #    App.Leds.GetObj('green').Set(1)
    #    ServerRun('0.0.0.0', 80)
    #else:
    #    print("cant connect Wi-Fi")
Main()
