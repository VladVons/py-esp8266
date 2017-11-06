#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---


# This file is executed on every boot (including wake-boot from deepsleep)

import esp
#import webrepl
#import machine
import gc
import micropython
#webrepl.start()

esp.osdebug(None)

gc.collect()
print('Pure MicroPython', 'MemFree', gc.mem_free(), 'MemAlloc', gc.mem_alloc())

# RAM for the emergency exception buffer
micropython.alloc_emergency_exception_buf(100)
