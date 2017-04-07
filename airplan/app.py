#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---

import log
import wlan
import api
import config
import serial
import serverudp
import common


class TApp:
    def __init__(self):
        self.Serial = serial.TSerial()
        
        Config = config.TConfig()
        Config.FileLoad('config.json')
        self.Conf = Config.GetItems()

        log.LogLevel = self.Conf.get('/App/LogLevel', 1);

        api.SetButton(api.cPinBtnPush,  self.OnButtonPush)

        self.TimerSock = common.TTimer(3000, self.OnSockTimeOut)

        #api.WatchDog(5000)
        #api.TimerCallback(3000, self.OnTimer)

    def OnButtonPush(self, aObj):
        log.Log(1, 'TApp.OnButtonPush', aObj);
        api.SetPinInv(api.cPinLedSys)

    def OnTimer(self, aObj):
        return None

    def OnSockTimeOut(self):
        log.Log(1, "OnSockTimeOut()", self.TimerSock.Cnt, "MemFree", api.GetMemFree())
        api.SetPinInv(api.cPinLedSys)
        return None

    def DefHandler(self):
        return self.TimerSock.Handle()

    def HandlerJson(self, aCaller, aData):
        if (aData):
            self.TimerSock.Update()
            api.SetPin(api.cPinLedSys, self.Serial.CntPacket % 2)
            Result = self.Serial.Parse(aData)
        else:
            Result = self.DefHandler()
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

            Server = serverudp.TServerUdpJson(ConfBind, ConfPort, ConfTimeOut)
            Server.BufSize = self.Conf.get('/Server/BufSize', 512)
            Server.Handler = self.HandlerJson
            Server.Run()
