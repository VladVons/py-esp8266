#!/usr/bin/python

import os
import struct
import hashlib

LogLevel= 3

def Log(aLevel, *aParam):
    if (aLevel <= LogLevel):
        print("LogLevel %d: %s" % (aLevel, list(aParam)))

def Print1():
    print("Print1")

def Print2(aMsg = "Print"):
    print("Print2", aMsg)
    return aMsg

def Print3(aPin, aValue, aStep):
    print('Print3', aPin, aValue, aStep)
    return aValue + aStep
  
def CallObj(aObj, aArgs):
    if (aArgs):
        Result = aObj(*aArgs)
    else:
        Result = aObj()
    return Result

def CallObjArr(*aArgs):
    Result = []
    Obj = aArgs[0]
    for i in range(1, len(aArgs)):
        Result.append(Obj(*aArgs[i]))
    return Result

def CallFuncArr(*aArgs):
    Args = list(aArgs)
    Args[0] = eval(Args[0])
    return CallObjArr(*Args)


print(dir(hashlib))

h='123456789012'
s=':'.join(h[i:i+2] for i in range(0, 12, 2))
print(s)

#Hash = hashlib.sha256('1234').hexdigest()
#print('Hash', Hash, len(Hash))
#SerialKey = "%s-%s" % (Hash[8:12], Hash[16:20])
#print(Hash, SerialKey, hash('11'))

#print(cl2, len(cl2), cl2[8:12], cl2[16:20])


#cl1 = hashlib.md5('123')
#print(dir(cl1))
#print(cl1.hexdigest(), cl1.digest(), cl1.name, cl1.digestsize)


#CallObj(Print2, [1])
#CallObj(CallObjArr, [Print2, [1], [2]])
#CallObj(CallFuncArr, ['Print2', [1], [2]])

#CallFuncArr('Print2', [1,2,3], ['a','b','c'], ['X', 'Y', 'Z'])
#OBResult = CallFuncArr(['Print3', [1, 'a', 'A'], [2, 'b', 'B'], [3, 'c', 'C'], [4, 'd', 'D']])
#Result = CallObjArr(Print2, [1], [2], [3])
#print(Result)
#Result = CallFuncArr(['Print2', [1], [2], [3]])
#print(Result)
#Result = CallFuncArr('Print1')
#print(Result)

#for i in range(30):
    #rand = int(os.urandom(2), 16)
    #rand = int(os.urandom(1).encode('hex'), 16)
#    print(rand)

#for i in range(20):
#    Rand = struct.unpack("I", os.urandom(4))[0] % 10
#    print(Rand)
