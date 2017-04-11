#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---

import log
import api
import serial
import sockserver
import common
import wlan

class TApp:
    def __init__(self, aConf):
        self.Conf = aConf
        self.Serial = serial.TSerial()

        log.LogLevel = self.Conf.get('/App/LogLevel', 3);

        api.SetButton(api.cPinBtnPush, self.IrqOnButtonPush)

        self.TimerSock   = common.TTimer(self.OnSockTimeOut, 2000)
        self.TimerButton = common.TTimerDebounce(self.OnButtonTimeOut, 1000, 250)

        #api.WatchDog(5000)
        #api.TimerCallback(3000, self.IrqOnTimer)

    def IrqOnButtonPush(self, aObj):
        log.Log(1, 'OnButtonPush', aObj);
  
        #common.DebouncePin(aObj)
        self.TimerButton.IncTag() 
        self.TimerButton.Update()  

        #api.SetPinInv(api.cPinLedSys)

    def IrqOnTimer(self, aObj):
        return None

    def OnButtonTimeOut(self):
        if (self.TimerButton.CntTag > 0):
            Tag = self.TimerButton.CntTag 
            print('')
            log.Log(1, "Tag", Tag)
            api.Dump(api.GetInfo())

            if   (Tag == 1):
               self.PinsInit()
            elif (Tag == 2):
                api.SetPin(api.cPinLedRed, 1) 
            elif (Tag == 3):
                api.SetPin(api.cPinLedGreen, 1) 
            self.TimerButton.CntTag = 0  

    def OnSockTimeOut(self):
        #log.Log(2, 'OnSockTimeOut()', self.TimerSock.CntCheck, 'MemFree', api.GetMemFree())
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
        Result = self.Conf.get('/WLan/Connect', False)
        if (Result):
            ESSID  = self.Conf.get('/WLan/ESSID', '')
            Paswd  = self.Conf.get('/WLan/Password', '')
            log.Log(1, 'ConnectWlan()', ESSID, Paswd)
            Result = api.ConnectWlan(ESSID,  Paswd)
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

        ConfBind     = self.Conf.get('/Server/Bind', '0.0.0.0')
        ConfPort     = self.Conf.get('/Server/Port', 51015)
        ConfTimeOut  = self.Conf.get('/Server/TimeOut', 0)
        ConfProtocol = self.Conf.get('/Server/Protocol', 'UDP')

        if (ConfProtocol == 'UDP'):
            Server = sockserver.TServerUdpJson(ConfBind, ConfPort, ConfTimeOut)
        else:
            Server = sockserver.TServerTCPJson(ConfBind, ConfPort, ConfTimeOut)

        Server.BufSize = self.Conf.get('/Server/BufSize', 512)
        Server.Handler = self.HandlerJson
        Server.Run()
