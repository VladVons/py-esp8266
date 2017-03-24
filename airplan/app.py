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

        api.SetPin(api.cPinLedSys, not api.GetPin(api.cPinLedSys))

    def HandlerJson(self, aCaller, aData):
        Name  = aData.get('Name')
        No    = aData.get('No')
        Value = aData.get('Value')
        print('HandlerJson', Name, No, Value)        

        if   (Name == "GetAdc"):
            Result = api.GetAdc()            
        elif (Name == "GetPin"):
            Result = api.GetPin(No)            
        elif (Name == "SetPin"):
            Result = api.SetPin(No, Value)            
        elif (Name == "GetPwm"):
            Result = api.GetPwm(No)
        elif (Name == "SetPwm"):
            Duty = aData.get('Duty')
            Result = api.SetPwm(No, Value, Duty)
        else:
            Result = 'Unhandl[ed'

        return Result  

    def ConnectWlan(self):
        Result = self.Conf.get('/WLan/Connect', True)
        if (Result):
            ESSD   = self.Conf.get('/WLan/ESSID')
            Paswd  = self.Conf.get('/WLan/Password')
            print("ConnectWlan", ESSD, Paswd)
            Result = wlan.Connect(ESSD,  Paswd)
            if (Result):
                print('Network', wlan.GetInfo())
                api.SetPins([api.cPinLedSys, api.cPinLedGreen, api.cPinLedBlue], 0)
                api.SetPin(api.cPinLedRed, 1)
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
