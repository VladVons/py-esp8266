#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---

import log
import api
import serial
import sockserver
import common


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

        self.SerialKeyTimer = common.GetRand(60 * 5, 60 * 3)
        self.SerialKeyOk    = (common.GetSerial() == self.Conf.get('/App/SerialKey'))

        #api.Dump(api.GetMethods('ubinascii'))

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

    def CheckSerialKey(self):
        Result = self.SerialKeyOk
        if (not Result):
            Result = (api.GetTicks() / 1000 < self.SerialKeyTimer)
            if (not Result):
                Result = (common.GetRand(10) > 3)
        return Result

    def HandlerDef(self):
        self.TimerButton.Handle()
        self.TimerSock.Handle()
        return None

    def HandlerJson(self, aCaller, aData):
        #log.Log(1, 'HandlerJson()', aData)
        if (aData):
            self.TimerSock.Update()
            if (self.CheckSerialKey()):
                api.SetPinInv(api.cPinLedSys)
                Result = self.Serial.Parse(aData)
            else:
                api.SetPinInv(api.cPinLedRed)
                #aData['Data'] = 'Wrong SerialKey'
                Result = aData
        else:
            Result = self.HandlerDef()
        return Result 

    def PinsInit(self):
        api.CallObjArr(api.SetPin, [api.cPinLedRed, 0], [api.cPinLedGreen, 0], [api.cPinLedBlue, 0])
        api.CallObjArr(api.SetPwmOff, [12], [13], [14], [15])

    def Listen(self):
        self.PinsInit()
        api.Dump(api.GetInfo())

        ConfBind     = self.Conf.get('/Server/Bind', '0.0.0.0')
        ConfPort     = self.Conf.get('/Server/Port', 51015)
        ConfTimeOut  = self.Conf.get('/Server/TimeOut', 0)
        ConfProtocol = self.Conf.get('/Server/Protocol', 'UDP')

        if (ConfProtocol == 'UDP'):
            SockServer = sockserver.TSockServerUdpJson(ConfBind, ConfPort, ConfTimeOut)
        else:
            SockServer = sockserver.TSockServerTCPJson(ConfBind, ConfPort, ConfTimeOut)
        self.Serial.AddObj("SetBufSize", SockServer.SetBufSize)

        SockServer.BufSize = self.Conf.get('/Server/BufSize', 512)
        SockServer.Handler = self.HandlerJson
        SockServer.Run()
