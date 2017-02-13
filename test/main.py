import gc
import ujson
import ubinascii
import ulog

#------------------------------------------
def MemFree():
    #gc.collect()
    print("Mem free a1", gc.mem_free()) # 28768

def Json():
    Data = b'{"data2":"hello"}'
    #Data = ubinascii.b2a_base64(Data)
    print('--1', Data)
    print('--2', ujson.loads(Data))

#MemFree()
Json()
