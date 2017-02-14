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
        return TFile.Load(Name)

    @staticmethod
    def FileList():
        return '\n'.join(TFile.List())

    @staticmethod
    def SetEssd(aName, aPassw):
        TWlan.SetEssd('vando-' + aName, aPassw)

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
            '/server?cmd=close\n'
            '/server?cmd=reset\n'
            '/server?cmd=mem\n'
        )
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

    def OnSocketHttp(self, aCaller, aUrl):
        Path = aUrl.get('_path')
        Dir  = aUrl.get('_dir')
        Log('TButton.OnHttpGet', Path, Dir)

        Result = 'unknown'
        if (Dir == '/help'):
            Result = TApi.Help()

        elif (Dir == '/led'):
            Result = 'OK'
            On  = int(aUrl.get('on', '1')) 
            Num = aUrl.get('num')
            if (Num):
                self.Leds.SetNo(int(Num), On)
            else:
                self.Leds.Set(On)

        elif (Dir == '/file'):
            Result = 'OK'
            Cmd  = aUrl.get('cmd') 
            if (Cmd == 'show'):
                Name  = aUrl.get('name', 'boot.py') 
                f = open(Name)
                Result = f.read()
                f.close()
            elif (Cmd == 'ls'):
                Result = '\n'.join(os.listdir())

        elif (Dir == '/server'):
            Result = 'OK'
            Cmd  = aUrl.get('cmd')
            if (Cmd == 'close'):
                aCaller.Close()
            elif (Cmd == 'reset'):
                machine.reset()
            elif (Cmd == 'mem'):
                gc.collect()
                Result = str(gc.mem_free())

        elif (Dir == '/pwm'):
            pin   = int(aUrl.get('pin', '5'))
            freq  = int(aUrl.get('freq', '50'))
            duty  = int(aUrl.get('duty', '100'))

            pwm = machine.PWM(machine.Pin(pin))
            pwm.freq(freq)
            pwm.duty(duty)
            #pwm.deinit()
            Result = '/pwm pin:%d, freq:%d, duty:%d' % (pin, pwm.freq(), pwm.duty())

        elif (Dir == '/adc'):
            adc = machine.ADC(0)
            Result = '/adc: %d' % (adc.read())

        return Result

    def Connect(self):
        Result = self.Conf['/WLan/Connect']
        if (Result):
            WLan = TWLan()
            Result = WLan.Connect(self.Conf['/WLan/ESSID'], self.Conf['/WLan/Password'])
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
            self.Server.CallBack = self.OnSocketHttp
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
