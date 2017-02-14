#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---

import os
import machine
import gc
#

from control import TPinIn
from led import *
from net import *
from common import *
from config import *

cPinBtnFlash = 0
cPinBtnPush  = 4

#micropython.alloc_emergency_exception_buf(128)

class TApi:
    @staticmethod
    def FileLoad(aName):
        return TFile.Load(aName)

    @staticmethod
    def FileList():
        return '\n'.join(TFile.List())

    @staticmethod
    def SetEssd(aName, aPassw):
        TWlan.SetEssd('vando-' + aName, aPassw)

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
        Result = '/pwm pin:%d, freq:%d, duty:%d' % (aPin, pwm.freq(), pwm.duty())

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

    @staticmethod
    def Help():
        Result = (
            '/led?num=x&on=x (set led num 0-3, on 0-1)\n'
            '/led?on=x (set all leds on 0-1)\n'
            '\n'
            '/pwm?pin=x&freq=x&duty=x (set pin freq 0-1023)\n'
            '\n'
            '/adc (get adc LDR value 0-1023)\n'
            '\n'
            '/file?cmd=show&name=xxx (show file xxx)\n'
            '/file?cmd=ls (list files) \n'
            '\n'
            '/machine?cmd=reset\n'
            '/machine?cmd=mem\n'
        )
        return Result

    @staticmethod
    def HttpEntry(aCaller, aUrl):
        Path = aUrl.get('_path')
        Dir  = aUrl.get('_dir')
        Log('TButton.OnHttpGet', Path, Dir)

        Result = 'unknown'
        if (Dir == '/help'):
            Result = TApi.Help()

        elif (Dir == '/led'):
            On  = int(aUrl.get('on', '0')) 
            Num = aUrl.get('num', '-1')
            TApi.SetLed(Num, On)
            Result = 'OK'

        elif (Dir == '/file'):
            Cmd  = aUrl.get('cmd') 
            if (Cmd == 'show'):
                Name  = aUrl.get('name') 
                Result = TApi.FileLoad(Name)
            elif (Cmd == 'ls'):
                Result = TApi.FileList()

        elif (Dir == '/machine'):
            Cmd  = aUrl.get('cmd') 
            if (Cmd == 'reset'):
                TApi.Reset()
            elif (Cmd == 'mem'):
                Result = str(TApi.GetMemFree())

        elif (Dir == '/pwm'):
            pin   = int(aUrl.get('pin', '5'))
            freq  = int(aUrl.get('freq', '50'))
            duty  = int(aUrl.get('duty', '100'))
            Result = TApi.SetPwm(pin, freq, duty)

        elif (Dir == '/adc'):
            Result = str(TApi.GetAdc())

        return Result

class TApp:
    def __init__(self):
        self.Server = None
        self.Leds   = TLeds()
        self.Cnt    = 0

        Config = TConfig()
        Config.LoadFile()
        self.Conf = Config.GetItems()
        #common.cLogSHow = self.Conf['/App/Debug']

        TPinIn(cPinBtnPush,  self.OnButtonPush, 'push')
        TPinIn(cPinBtnFlash, self.OnButtonFlash, 'flash')
        #TTimer(0, self.OnTimer, 2000)

    def OnTimer(self, aObj):
        Log('TApp.OnTimer');

        self.Leds.Toggle()
        #self.Leds[0].Toggle()

    def OnButtonPush(self, aObj):
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


    def Connect(self):
        Result = self.Conf['/WLan/Connect']
        if (Result):
            WLan = TWLan()
            Result = WLan.Connect(self.Conf['/WLan/ESSID'], self.Conf['/WLan/Password'])
            #Result = WLan.Connect('ASUS', '55886209')
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
            self.Server = TServerHttp(self.Conf['/Server/Bind'], self.Conf['/Server/Port'])
            self.Server.CallBack = TApi.HttpEntry
            self.Server.Run()

    def TestLeds(self, aCount):
        Log('TApp.TestLeds', aCount)
        for i in range(aCount):
            self.Leds.Toggle()

    def TestSpeed(self, aCount):
        import ujson
        import time

        TimeStart = time.ticks_ms()
        for i in range(aCount):
            #DataIn  = ujson.dumps( {'data': i} )
            #DataOut = ujson.loads(DataIn)

            Val = int(i % 2)
            self.Leds.Set(Val)

        print('MSec', time.ticks_ms() - TimeStart)
