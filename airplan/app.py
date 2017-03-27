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
        self.CntCall  = 0
        self.LastCall = 0

        Config = TConfig()
        Config.FileLoad('config.json')
        self.Conf = Config.GetItems()

        api.SetButton(api.cPinBtnPush,  self.OnButtonPush)

        #api.WatchDog(5000)
        #api.TimerCallback(3000, self.OnTimer)

    def OnButtonPush(self, aObj):
        Log('TApp.OnButtonPush', aObj);
        api.SetPin(api.cPinLedSys, not api.GetPin(api.cPinLedSys))

    def OnTimer(self, aObj):
        Ticks = api.GetTicks()
        if (Ticks - self.LastCall > 10000):
            self.LastCall = Ticks 
            api.SetPinInv(api.cPinLedSys)
            self.DefHandler()

    def DefHandler(self):
        print ("DefHandler", "CntCall", self.CntCall, "MemFree", api.GetMemFree())
        return None

    def Parse(self, aData):
        self.CntCall += 1 
        self.LastCall = api.GetTicks()

        Name  = aData.get('Name')
        Item  = aData.get('Item')
        Value = aData.get('Value')
        print('Parse Cnt:', self.CntCall, "Name:", Name, "Item;", Item, "Value:", Value)

        if (Name):
            try:
                Obj = getattr(api, Name)
            except:
                Obj = None

            if (Obj):
                if (Item != None and Value != None):
                    Result = Obj(Item, Value)
                elif (Item != None):
                    Result = Obj(Item)
                elif (Value != None):
                    Result = Obj(Value)
                else:
                    Result = Obj()
            else:
                Result = 'Error: Unknown Name'
                print(Result) 
        else:
            Result = self.DefHandler()
        return {"Name": Name, "Result": Result}

    def HandlerJson(self, aCaller, aData):
        # array of requests
        if (isinstance(aData, list)):
            Result = []
            for Data in aData:
                Result.append(self.Parse(Data))
        else:
            Result = self.Parse(aData)
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
            print('connect AP. Password: micropythoN')
            Result = True
        return Result

    def Listen(self):
        if (self.ConnectWlan()):
            Bind    = self.Conf.get('/Server/Bind', '0.0.0.0')
            Port    = self.Conf.get('/Server/Port', 51015)
            TimeOut = self.Conf.get('/Server/TimeOut', -1)

            Server = TServerUdpJson(Bind, Port, TimeOut)
            Server.BufSize = self.Conf.get('/Server/BufSize', 512)
            Server.Handler = self.HandlerJson
            Server.Run()
