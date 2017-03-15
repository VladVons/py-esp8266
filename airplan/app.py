#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---

import wlan
import api
from server_udp import TServerUdpJson
from config     import TConfig
from common import Log, cLogSHow 


class TApp:
    def __init__(self):
        self.Server = None

        Config = TConfig()
        Config.FileLoad('config.json')
        self.Conf = Config.GetItems()

        api.SetButton(api.cPinBtnPush,  self.OnButtonPush)

    def OnButtonPush(self, aObj):
        Log('TApp.OnButtonPush', aObj);

        api.SetLed(api.cPinLedSys, not api.GetLed(api.cPinLedSys))

    def HandlerJson(self, aCaller, aData):
        Log('Tapp.HandlerJson', aData)

        Name  = aData.get('Name')
        No    = aData.get('No')
        Value = aData.get('Value')
        print(Name, No, Value)        

        if (Name == "Lamp"):
            api.SetLed(No, Value)            
        elif (Name == "MotorDC"):
            api.SetPwm(No, Value, 10)            

        return 'OK'

    def ConnectWlan(self):
        Result = self.Conf.get('/WLan/Connect', True)
        if (Result):
            ESSD   = self.Conf.get('/WLan/ESSID')
            Paswd  = self.Conf.get('/WLan/Password')
            print("ConnectWlan", ESSD, Paswd)
            Result = wlan.Connect(ESSD,  Paswd)
            if (Result):
                api.SetLed(api.cPinLedGreen, 1)
                print('Network', wlan.GetInfo())
            else:
                print('Cant connect WiFi')
        else:
            print('connect to me via AP. Password: micropythoN')
            Result = True
        return Result

    def Listen(self):
        if (self.ConnectWlan()):
            self.Server = TServerUdpJson(self.Conf.get('/Server/Bind', '0.0.0.0'), self.Conf.get('/Server/Port', 51015))
            self.Server.Handler = self.HandlerJson
            self.Server.Run()
