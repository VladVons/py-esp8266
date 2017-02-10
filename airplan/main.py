#---VladVons@gmail.com
# 04.02.17
#---

#http://www.schatenseite.de/en/2016/04/22/esp8266-witty-cloud-module/
#https://docs.micropython.org/en/latest/esp8266/esp8266/quickref.html


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

        Result = ''
        if (Dir == '/led'):
            Result = 'OK'
            On  = int(aUrl.get('on', '1')) 
            Num = int(aUrl.get('num', '0'))
            #print('num', Num, 'on', On)
            self.Leds.SetNo(Num, On)
        elif (Dir == '/all'):
            Result = 'OK'
            On  = int(aUrl.get('on', '1')) 
            #print('on', On)
            self.Leds.Set(On)
        elif (Dir == '/file'):
            Result = 'OK'
            File  = aUrl.get('name', 'boot.py') 
            print('111', File)
            f = open(File, 'rb')
            Result = f.read()
            f.close()
        elif (Dir == '/exit'):
            Result = 'OK'
            aCaller.Active = False
        elif (Dir == '/pwm'):
            pin   = int(aUrl.get('pin', '5')) 
            freq  = int(aUrl.get('freq', '50')) 
            duty  = int(aUrl.get('duty', '100')) 

            pwm = machine.PWM(machine.Pin(pin))
            pwm.freq(freq)
            pwm.duty(duty)
            #pwm.deinit()

            Result = 'PWM pin:{}, freq:{}, duty:{}' % (pin, freq, duty)
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


    def TestPwm(self):
        pwm0 = machine.PWM(machine.Pin(5))

        print('--1a', pwm0.freq())
        pwm0.freq(100)
        print('--1b', pwm0.freq())

        print('--2a', pwm0.duty())
        pwm0.duty(20)
        print('--2b', pwm0.duty())

        pwm0.deinit()


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

    #gc.collect()
    #print("Mem free a1", gc.mem_free())

    App = TApp()
    App.TestLeds(1*4)
    #App.TestPwm()
    App.Connect()
    #App.SleepAlways()

    # Here while pressing button raise error: MemoryError

    #gc.collect()
    #print("Mem free b", gc.mem_free())

Main()
