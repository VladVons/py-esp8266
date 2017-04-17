import machine
import ustruct
import os
import gc
import uhashlib
import ubinascii
#
import log
import wlan
import libtime


def Dump(aValue, aPref = ''):
    if (isinstance(aValue, dict)):
        for Key in aValue:
            Dump(aValue[Key], aPref + '/' + Key)
    elif (isinstance(aValue, list)):
        for Value in aValue:
            Dump(Value, aPref)
    else:
        print(aPref, aValue)

def Exec(aValue = 'Result = (2+3)*2'):
    Result = None
    Vars   = {}
    try:
        exec(aValue, globals(), Vars)
        Result = Vars.get('Result')
    except Exception as e:
        log.Log(0, e)
        Result = e
    return Result

def GetRand(aMin = 0, aMax = 65536):
    Rand = ustruct.unpack("I", os.urandom(4))[0]
    return aMin + (Rand % (aMax - aMin))

def GetSerial():
    Bytes = uhashlib.sha256(wlan.GetMac()).digest()
    Hash  = ubinascii.hexlify(Bytes).decode('utf-8')
    return "%s-%s-%s-%s" % (Hash[8:12], Hash[16:20], Hash[24:28], Hash[32:36])

def GetMethods(aModule):
    return dir(__import__(aModule))


# --- Mem
def MemGarbage():
    gc.collect()

def GetMemFree():
    MemGarbage()
    return gc.mem_free()

def GetMemAlloc():
    MemGarbage()
    return gc.mem_alloc()


# --- CPU
def Reset():
    machine.reset()

def CpuBurst(aValue = True):
    if (aValue):
        machine.freq(160 * 1000000)
    else:
        machine.freq(80 * 1000000)
    return machine.freq()

#def GetMachineId():
#    return machine.unique_id().decode("utf-8")

