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
        self.CntCall    = 0
        self.CntPacket  = 0
        self.LastPacket = 0

        Config = config.TConfig()
        Config.FileLoad('config.json')
        self.Conf = Config.GetItems()

        log.LogLevel = self.Conf.get('/App/LogLevel', 1);

        api.SetButton(api.cPinBtnPush,  self.OnButtonPush)

        #api.WatchDog(5000)
        #api.TimerCallback(3000, self.OnTimer)

    def GetInfo(self):
        Result = "CntPacket %d, CntCall %d" % (self.CntPacket, self.CntCall)
        print(Result)
        return Result

    def OnButtonPush(self, aObj):
        log.Log(2, 'TApp.OnButtonPush', aObj);
        api.SetPin(api.cPinLedSys, not api.GetPin(api.cPinLedSys))

    def OnTimer(self, aObj):
        Ticks = api.GetTicks()
        if (Ticks - self.LastPacket > 10000):
            self.LastPacket = Ticks 
            api.SetPinInv(api.cPinLedSys)
            self.DefHandler("OnTimer")

    def DefHandler(self, aData):
        log.Log(1, "DefHandler()", "CntCall", self.CntCall, "MemFree", api.GetMemFree())
        return None

    def Parse(self, aData):
        aClass = aData.get('Class', None)
        aFunc  = aData.get('Func',  None)
        aArgs  = aData.get('Args',  None)

        self.CntCall += 1 
        log.Log(2, 'Parse()', 'CntCall', self.CntCall, 'Func', aFunc, 'Args', aArgs)

        if (aFunc):
            try:
                if (aClass):
                    Class = globals()[aClass]()
                else:
                    Class = api
                Obj = getattr(Class, aFunc)
            except:
                Obj = None

            if (Obj):
                if (aArgs):
                    ArgCnt = len(aArgs)
                    if   (ArgCnt == 1):
                        Result = Obj(aArgs[0])
                    elif (ArgCnt == 2):
                        Result = Obj(aArgs[0], aArgs[1])
                    elif (ArgCnt == 3):
                        Result = Obj(aArgs[0], aArgs[1], aArgs[2])
                    else:
                        Result = Obj()
                else:
                    Result = Obj()
            else:
                Result = 'Error: Unknown Func ' + aFunc
                print(Result) 
        else:
            Result = self.DefHandler(aData)
        return {"Func": aFunc, "Args": aArgs, "Result": Result}

    def HandlerJson(self, aCaller, aData):
        self.CntPacket += 1;
        self.LastPacket = api.GetTicks()
        log.Log(1, "HandlerJson()", "CntPacket", self.CntPacket,  'LastPacket', self.LastPacket)

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
            ESSID  = self.Conf.get('/WLan/ESSID')
            Paswd  = self.Conf.get('/WLan/Password')
            print("ConnectWlan", ESSID, Paswd)
            Result = wlan.Connect(ESSID,  Paswd)
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

            ConfBind    = self.Conf.get('/Server/Bind', '0.0.0.0')
            ConfPort    = self.Conf.get('/Server/Port', 51015)
            ConfTimeOut = self.Conf.get('/Server/TimeOut', -1)

            Server = TServerUdpJson(ConfBind, ConfPort, ConfTimeOut)
            Server.BufSize = self.Conf.get('/Server/BufSize', 512)
            Server.Handler = self.HandlerJson
            Server.Run()
