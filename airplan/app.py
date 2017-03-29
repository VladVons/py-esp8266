#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---

import log
import wlan
import api
import config
from server_udp import TServerUdpJson


class TApp:
    def __init__(self):
        self.CntCall  = 0
        self.LastCall = 0

        Config = config.TConfig()
        Config.FileLoad('config.json')
        self.Conf = Config.GetItems()

        log.LogLevel = self.Conf.get('/App/LogLevel', 1);        

        api.SetButton(api.cPinBtnPush,  self.OnButtonPush)

        #api.WatchDog(5000)
        #api.TimerCallback(3000, self.OnTimer)

    def OnButtonPush(self, aObj):
        log.Log(2, 'TApp.OnButtonPush', aObj);
        api.SetPin(api.cPinLedSys, not api.GetPin(api.cPinLedSys))

    def OnTimer(self, aObj):
        Ticks = api.GetTicks()
        if (Ticks - self.LastCall > 10000):
            self.LastCall = Ticks 
            api.SetPinInv(api.cPinLedSys)
            self.DefHandler("OnTimer")

    def DefHandler(self, aData):
        log.Log(1, "DefHandler", "CntCall", self.CntCall, "MemFree", api.GetMemFree())
        return None

    def Parse(self, aData):
        self.CntCall += 1 
        self.LastCall = api.GetTicks()

        Func  = aData.get('Func', None)
        Args  = aData.get('Args', None)
        log.Log(1, 'Parse Cnt:', self.CntCall, "Func:", Func, "Args;", Args)

        if (Func):
            try:
                Obj = getattr(api, Func)
            except:
                Obj = None

            if (Obj):
                if (Args):
                    ArgCnt = len(Args)
                    if   (ArgCnt == 1):
                        Result = Obj(Args[0])
                    elif (ArgCnt == 2):
                        Result = Obj(Args[0], Args[1])
                    elif (ArgCnt == 3):
                        Result = Obj(Args[0], Args[1], Args[2])
                    else:
                        Result = Obj()
                else:
                    Result = Obj()
            else:
                Result = 'Error: Unknown Func ' + Func
                print(Result) 
        else:
            Result = self.DefHandler(aData)
        return {"Name": Func, "Result": Result}

    def HandlerJson(self, aCaller, aData):
        # array of requests
        if (isinstance(aData, list)):
            Result = []
            for Data in aData:
                Result.append(self.Parse(Data))
        else:
            Result = self.Parse(aData)
        return Result

    def PinsInit(self):
        api.SetPinArr(api.ArrLed , 0)
        api.SetPwmOffArr(api.ArrMotor1)
        api.SetPwmOffArr(api.ArrMotor2)

    def ConnectWlan(self):
        Result = self.Conf.get('/WLan/Connect', True)
        if (Result):
            ESSD   = self.Conf.get('/WLan/ESSID')
            Paswd  = self.Conf.get('/WLan/Password')
            print("ConnectWlan", ESSD, Paswd)
            Result = wlan.Connect(ESSD,  Paswd)
            if (Result):
                print('Network', wlan.GetInfo())
            else:
                print('Cant connect WiFi')
        else:
            print('connect AP. Password: micropythoN')
            Result = True
        return Result

    def Listen(self):
        if (self.ConnectWlan()):
            self.PinsInit()

            Bind    = self.Conf.get('/Server/Bind', '0.0.0.0')
            Port    = self.Conf.get('/Server/Port', 51015)
            TimeOut = self.Conf.get('/Server/TimeOut', -1)

            Server = TServerUdpJson(Bind, Port, TimeOut)
            Server.BufSize = self.Conf.get('/Server/BufSize', 512)
            Server.Handler = self.HandlerJson
            Server.Run()
