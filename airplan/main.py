#---VladVons@gmail.com
# 04.02.17
# micropython.OD ESP8266
#---

# http://micropython.org/download#esp8266
# http://www.schatenseite.de/en/2016/04/22/esp8266-witty-cloud-module/
# https://docs.micropython.org/en/latest/esp8266/esp8266/quickref.html

import os
import time
import machine
import gc
#

from button import *
from led import *
from net import *
from timer import *
from common import *

#micropython.alloc_emergency_exception_buf(128)

#------------------------------------------
class TApp:
    def __init__(self):
        self.Server = None
        self.Leds   = TLeds()

        TButton(cPioBtnPush,  self.OnButtonPush)
        TButton(cPioBtnFlash, self.OnButtonFlash)
        #TTimer(0, self.OnTimer, 2000)

    def OnTimer(self, aObj):
        Log('TApp.OnTimer');

        self.Leds.Toggle()
        #self.Leds[0].Toggle()

    def OnButtonPush(self, aObj):
        Log()
        Log('TApp.OnButtonPush', aObj, self.Leds.Idx);

        self.Leds.Toggle()
        if (self.Leds.Idx == self.Leds.GetCount()):
            self.Leds.Set(True)

    def OnButtonFlash(self, aObj):
        Log('TApp.OnButtonFlash')

        #if (self.Server):
        #    self.Server.Close()

        #machine.reset()

        adc = machine.ADC(0)
        print('ADC', adc.read())

    def OnHttpGet(self, aCaller, aUrl):
        Path = aUrl.get('_path')
        Dir  = aUrl.get('_dir')
        Log('TButton.OnHttpGet', Path, Dir)

        Result = 'unknown'
        if (Dir == '/help'):
            Result = (
                'Ussage:\n'
                '/help (this help)\n'
                '\n'
                'pins:\n'
                '00 - button flush\n'
                '02 - led    sys\n'
                '04 - button push\n'
                '05 - unused\n'
                '12 - led    green\n'
                '13 - led    blue\n'
                '14 - unused\n'
                '15 - led    red \n'
                '16 - unused\n'
                '\n'
                '/led?num=x&on=x (set led num 0-3, on 0-1)\n'
                '/led?on=x (set all leds on 0-1)\n'
                '\n'
                '/pwm?pin=x&freq=x&duty=x (set pin 0,2,4,5,12,13,14,15,16 freq 0-1023)\n'
                '\n'
                '/adc (get adc LDR value 0-1023)\n'
                '\n'
                '/file?cmd=show&name=xxx (show file xxx)\n'
                '/file?cmd=ls (list files) \n'
                '\n'
                '/server?cmd=close\n'
                '/server?cmd=reset\n'
                '\n'
                '/led?num=x&on=x\n'
                    )
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

        elif (Dir == '/pwm'):
            pin   = int(aUrl.get('pin', '5'))
            freq  = int(aUrl.get('freq', '50'))
            duty  = int(aUrl.get('duty', '100'))

            pwm = machine.PWM(machine.Pin(pin))
            pwm.freq(freq)
            pwm.duty(duty)
            #pwm.deinit()

            Result = '/pwm pin:%d, freq:%d, duty:%d' % (pin, pwm.freq(), pwm.duty())
            Log(Result)

        elif (Dir == '/adc'):
            adc = machine.ADC(0)
            Result = '/adc: %d' % (adc.read())
            Log(Result)

        return Result

    def Connect(self):
        WLan = TWLan()
        Conn = WLan.Connect('R3-0976646510', '19710000')
        #Conn = WLan.Connect('L90_VladVons', '19710000')
        #Conn = WLan.Connect('ASUS', '55886209')
        if (Conn):
            print('Network', WLan.GetInfo())
            self.Server = TServer()
            self.Server.CallBack = self.OnHttpGet
            self.Server.Run()
        else:
            print('Cant connect WiFI')

    def TestLeds(self, aCount):
        Log('TApp.TestLeds', aCount)

        for i in range(aCount):
            self.Leds.Toggle()
            if (self.Leds.Idx == 0):
                self.Leds.Set(True)
                time.sleep_ms(1000)
                self.Leds.Set(False)


    def SleepAlways():
        while True:
            # dont burn CPU
            time.sleep_ms(100)


#------------------------------------------
def Main():
    #time.sleep_ms(5000)

    gc.collect()
    print("Mem free a1", gc.mem_free())

    App = TApp()
    App.TestLeds(1*4)
    App.Connect()
    #App.SleepAlways()

    # Here while pressing button raise error: MemoryError

    #gc.collect()
    #print("Mem free b", gc.mem_free())

Main()
