#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---

import os
import machine
import gc
#

def HandlerHttp(aCaller, aUrl):
    Path = aUrl.get('_path')
    Dir  = aUrl.get('_dir')
    Log('TButton.OnHttpGet', Path, Dir)

    Result = 'unknown'
    if (Dir == '/help'):
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
        Result = 'freq:%d, duty:%d' % TApi.SetPwm(pin, freq, duty)

    elif (Dir == '/adc'):
        Result = str(TApi.GetAdc())

    return Result
