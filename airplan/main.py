#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---

#from wlan2 import TWLan
#import wlan
import wlan
#from server_udp import TServerUdpJson
from server_tcp import TServerTcpHttp

#import net

#from app import TApp
#
#import urequests
#import urllib
#import micropython


def Main():
    #gc.collect()
    print("Mem free", gc.mem_free())
    #print("Mem info", micropython.mem_info())

    #print(dir(machine))
    #print("urllib", dir(urllib))
    #print("urequests", dir(urequests))

    #App = TApp()
    #App.TestLeds(1*4)
    #App.TestSpeed(1000)
    #App.Listen()

    #wlan.SetEssd('PinkFloyd', '19790000')
    print(wlan.Scan())

    Con = wlan.Connect('R3-0976646510', '19710000')
    if (Con):
        print('Network1', wlan.GetInfo())
        #Server = TServerUdpJson('0.0.0.0', 80)
        Server = TServerTcpHttp('0.0.0.0', 80)
        Server.Handler = Http
        Server.Run()
        #print('Network', net.TWLan.GetInfo())
        ##App.Leds.GetObj('green').Set(1)
        #net.ServerRun('0.0.0.0', 80)
    else:
        print("cant connect Wi-Fi")

    print("Mem free", gc.mem_free())


Main()
