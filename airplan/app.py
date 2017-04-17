#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---

import log
import api
import lib
import libpin
import libtime
import serialize
import sockserver
import util
import const


class TApp:
    def __init__(self, aConf):
        self.Conf = aConf

        self.Serialize = serialize.TSerialize()

        log.LogLevel = self.Conf.get('/App/LogLevel', 3);
        lib.CpuBurst(self.Conf.get('/App/CpuBurst', False));

        libpin.SetButton(const.PinBtnPush, self.IrqOnButtonPush)

        self.TimerSock   = libtime.TTimer(self.OnSockTimeOut, 2000)
        self.TimerButton = libtime.TTimerDebounce(self.OnButtonTimeOut, 1000, 250)

        #api.WatchDog(5000)
        #api.TimerCallback(3000, self.IrqOnTimer)

        self.SerialKeyTimer = lib.GetRand(60 * 5, 60 * 3)
        self.SerialKeyOk    = (lib.GetSerial() == self.Conf.get('/App/SerialKey'))
        #print('SerialKey', self.Conf.get('/App/SerialKey'), lib.GetSerial())

        #lib.Dump(lib.GetMethods('ubinascii'))
        #lib.CpuBurst(True)
        #lib.Dump(util.SpeedTest(1 * 1000, const.PinLedSys))

    def IrqOnButtonPush(self, aObj):
        log.Log(1, 'OnButtonPush', aObj);
  
        #libtyme..DebouncePin(aObj)
        self.TimerButton.IncTag() 
        self.TimerButton.Update()  

        #libpin.SetPinInv(const.PinLedSys)

    def IrqOnTimer(self, aObj):
        return None

    def OnButtonTimeOut(self):
        if (self.TimerButton.CntTag > 0):
            Tag = self.TimerButton.CntTag 
            log.Log(1, "Tag", Tag)
            lib.Dump(api.GetInfo())

            if   (Tag == 1):
               self.PinsInit()
            elif (Tag == 2):
                libpin.SetPin(const.PinLedRed, 1) 
            elif (Tag == 3):
                libpin.SetPin(const.PinLedGreen, 1) 
            self.TimerButton.CntTag = 0  

    def OnSockTimeOut(self):
        #log.Log(2, 'OnSockTimeOut()', self.TimerSock.CntCheck, 'MemFree', lib.GetMemFree())
        libpin.SetPinInv(const.PinLedSys)

    def CheckSerialKey(self):
        Result = self.SerialKeyOk
        if (not Result):
            Result = (libtime.GetTicks() / 1000 < self.SerialKeyTimer)
            if (not Result):
                Result = (lib.GetRand(10) > 3)
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
                libpin.SetPinInv(const.PinLedSys)
                Result = self.Serialize.Parse(aData)
            else:
                libpin.SetPinInv(const.PinLedRed)
                #aData['Data'] = 'Wrong SerialKey'
                Result = aData
        else:
            Result = self.HandlerDef()
        return Result 

    def PinsInit(self):
        api.CallObjArr(api.SetPin, [const.PinLedRed, 0], [const.PinLedGreen, 0], [const.PinLedBlue, 0])
        api.CallObjArr(api.SetPwmOff, [const.MotorDC1A], [const.MotorDC1B], [const.MotorDC2A], [const.MotorDC2B])

    def Listen(self):
        self.PinsInit()

        print('')
        lib.Dump(api.GetInfo())

        ConfBind     = self.Conf.get('/Server/Bind', '0.0.0.0')
        ConfPort     = self.Conf.get('/Server/Port', 51015)
        ConfTimeOut  = self.Conf.get('/Server/TimeOut', 0)
        ConfProtocol = self.Conf.get('/Server/Protocol', 'UDP')

        if (ConfProtocol == 'UDP'):
            SockServer = sockserver.TSockServerUdpJson(ConfBind, ConfPort, ConfTimeOut)
        else:
            SockServer = sockserver.TSockServerTCPJson(ConfBind, ConfPort, ConfTimeOut)

        self.Serialize.AddObj("SetBufSize", SockServer.SetBufSize)

        SockServer.BufSize = self.Conf.get('/Server/BufSize', 512)
        SockServer.Handler = self.HandlerJson
        SockServer.Run()
