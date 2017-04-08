#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---

import log
import api
import serial
import serverudp
import common
import wlan

class TApp:
    def __init__(self, aConf):
        self.Conf = aConf
        self.Serial = serial.TSerial()

        log.LogLevel = self.Conf.get('/App/LogLevel', 1);

        api.SetButton(api.cPinBtnPush, self.IrqOnButtonPush)

        self.TimerSock   = common.TTimer(2000, self.OnSockTimeOut)
        self.TimerButton = common.TTimer(1000, self.OnButtonTimeOut)

        #api.WatchDog(5000)
        #api.TimerCallback(3000, self.IrqOnTimer)

    def IrqOnButtonPush(self, aObj):
        log.Log(1, 'OnButtonPush', aObj);
  
        #common.DebouncePin(aObj)
        self.TimerButton.IncTagDebounce(1, 200) 
        self.TimerButton.Update()  

        #api.SetPinInv(api.cPinLedSys)

    def IrqOnTimer(self, aObj):
        return None

    def OnButtonTimeOut(self):
        if (self.TimerButton.Tag > 0):
            Tag = self.TimerButton.Tag 
            log.Log(1, 'OnButtonTimeOut()', Tag, 'MemFree', api.GetMemFree())

            if   (Tag == 1):
               self.PinsInit()
            elif (Tag == 2):
                api.SetPin(api.cPinLedRed, 1) 
            elif (Tag == 3):
                api.SetPin(api.cPinLedGreen, 1) 
            self.TimerButton.Tag = 0  

    def OnSockTimeOut(self):
        #log.Log(1, 'OnSockTimeOut()', self.TimerSock.CntCheck, 'MemFree', api.GetMemFree())
        api.SetPinInv(api.cPinLedSys)

    def HandlerDef(self):
        self.TimerButton.Handle()
        self.TimerSock.Handle()
        return None

    def HandlerJson(self, aCaller, aData):
        if (aData):
            self.TimerSock.Update()
            api.SetPin(api.cPinLedSys, self.Serial.CntPacket % 2)
            Result = self.Serial.Parse(aData)
        else:
            Result = self.HandlerDef()
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
            log.Log(1, 'ConnectWlan()', ESSID, Paswd)
            Result = api.Connect(ESSID,  Paswd)
            if (Result):
                log.Log(1, 'Network', wlan.GetInfo())
            else:
                log.Log(1, 'Cant connect WiFi')
        else:
            log.Log(1, 'connect AP. Password: micropythoN')
            Result = True
        return Result

    def Listen(self):
        self.PinsInit()

        ConfBind    = self.Conf.get('/Server/Bind', '0.0.0.0')
        ConfPort    = self.Conf.get('/Server/Port', 51015)
        ConfTimeOut = self.Conf.get('/Server/TimeOut', -1)

        Server = serverudp.TServerUdpJson(ConfBind, ConfPort, ConfTimeOut)
        Server.BufSize = self.Conf.get('/Server/BufSize', 512)
        Server.Handler = self.HandlerJson
        Server.Run()
