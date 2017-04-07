#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---

import time
import machine
#
#import urequests
#import urllib
#import micropython
#
#from wlan2 import TWLan
#import wlan

def Main1():
    #time.sleep_ms(3000)

    #gc.collect()
    print("Mem free", gc.mem_free())
    #print("Mem info", micropython.mem_info())

    #print(dir(machine))
    #print("urllib", dir(urllib))
    #print("urequests", dir(urequests))


def Main2():
    for Pin in [14]:
        print('Pin', Pin)
        servo = machine.PWM(machine.Pin(Pin), freq = 50)
        for Duty in [40, 115, 77]:
            print('Pin', Pin, 'Duty', Duty)
            servo.duty(Duty)
            time.sleep_ms(1000) 

Main2()
