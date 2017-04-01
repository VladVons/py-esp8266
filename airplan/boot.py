#---VladVons@gmail.com
# 04.02.17
# micropython ESP8266
#---


# This file is executed on every boot (including wake-boot from deepsleep)

#import esp
#esp.osdebug(None)
import gc
#import webrepl
#webrepl.start()

gc.collect()
print("MemFree", gc.mem_free(), "MemAlloc", gc.mem_alloc())
print("Hello from ESP8266 MicroPython")
