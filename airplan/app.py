#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---

import wlan
from server_udp import TServerUdpJson
from config     import TConfig
from control    import TPinIn
from common import Log
from led import *

cPinBtnFlash = 0
cPinBtnPush  = 4

#micropython.alloc_emergency_exception_buf(128)

class TApi:
    @staticmethod
    def FileLoad(aName):
        return fs.FileLoad(aName)

    @staticmethod
    def FileList():
        return '\n'.join(fs.FileList())

    @staticmethod
    def SetEssd(aName, aPassw):
        wlan.SetEssd('vando-' + aName, aPassw)

    @staticmethod
    def SetLed(aLeds, aNum, aOn):
        if (aNum == -1):
            aLeds.Set(aOn)
        else:
            aLeds.SetNo(aNum, aOn)

    @staticmethod
    def SetPwm(aPin, aFreq, aDuty):
        pwm = machine.PWM(machine.Pin(aPin))
        pwm.freq(aFreq)
        pwm.duty(aDuty)
        #pwm.deinit()
        return (pwm.freq(), pwm.duty())

    @staticmethod
    def GetAdc():
        adc = machine.ADC(0)
        return adc.read()

    @staticmethod
    def GetMemFree():
        gc.collect()
        return gc.mem_free()

    @staticmethod
    def Reset():
        machine.reset()


class TApp:
    def __init__(self):
        self.Server = None
        self.Leds   = TLeds()
        self.Cnt    = 0

        Config = TConfig()
        Config.FileLoad()
        self.Conf = Config.GetItems()

        global cLogSHow
        cLogSHow = self.Conf['/App/Debug']

        TPinIn(cPinBtnPush,  self.OnButtonPush, 'push')
        #TPinIn(cPinBtnFlash, self.OnButtonFlash, 'flash')
        #TTimer(0, self.OnTimer, 2000)

    async def OnButtonPush(self, aObj):
        Log('TApp.OnButtonPush', aObj);

        self.Leds.Toggle()
        if (self.Leds.Idx == self.Leds.GetCount()):
            self.Leds.Set(True)

    def OnButtonFlash(self, aObj):
        print('TApp.OnButtonFlash.OK')
        Log('TApp.OnButtonFlash.MemoryError')

        #if (self.Server):
        #    self.Server.Close()

    def OnSocketJson(self, aCaller, aData):
        self.Cnt += 1
        Val = int(self.Cnt % 2)

        #self.Leds.GetObj('red').Set(Val)
        self.Leds.Set(Val)
        return 'answer: ' + aData.get('data')


    def ConnectWiFi(self):
        Result = self.Conf.get('/WLan/Connect', true)
        if (Result):
            Result = wlan.Connect(self.Conf.get('/WLan/ESSID'), self.Conf.get('/WLan/Password'))
            if (Result):
                self.Leds.GetObj('green').Set(1)
                print('Network', WLan.GetInfo())
            else:
                print('Cant connect WiFi')
        else:
            print('connect to me via AP. Password: micropythoN')
            Result = True
        return Result

    def Listen(self):
        if (self.Connect()):
            self.Server = TServerHttp(self.Conf.get('/Server/Bind', '0.0.0.0'), self.Conf.get('/Server/Port', 80))
            self.Server.Handler = TApi.HttpEntry
            self.Server.Run()

    def TestLeds(self, aCount):
        Log('TApp.TestLeds', aCount)
        for i in range(aCount):
            self.Leds.Toggle()
