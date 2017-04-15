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

def Tips():
    #https://habrahabr.ru/post/85459/
    #https://habrahabr.ru/post/95721/

    print('\nset ')
    arr = [1, 2, 3, 3, 4, 1, 4, 3]
    print('arr', arr, 'uniq', list(set(arr)))

    print('\nmax')
    arr = [1, 2, 3, 3, 4, 1]
    print('arr', arr, 'max',  max(arr))

    print('\nmin')
    arr = ['one', 'two', 'three', 'four', 'fiwe', 'six']
    print('arr', arr, 'min', min(arr))

    print('\nzip')
    arr1 = ['a', 'b', 'c']
    arr2 = [1,   2,   3, 4]
    arr3 = ['one', 'two', 'three']
    zipped = zip(arr1, arr2, arr3)
    print('arr1', arr1, 'arr2', arr2, 'arr3', arr3, 'zip', zipped)

    print('\nall')
    arr = [1, 2, 3, 4, 5]
    if (all(item < 10 for item in arr)):
        print 'all items < 10'

    print('\nany')
    arr = [1, 2, 3, 4, 5]
    if (any(item == 3 for item in arr)):
        print('found item is 3')

    print('\nenumerate')
    arr = ['a', 'b', 'c', 'd', 'e']
    for i, string in enumerate(arr):
        print ('enumerate', i, string)

    print('\ndict')
    arr = dict(a = 1, b = 2, c = dict(x = 1, y = 2))
    print('arr', arr) 

    print('\ndict to items')
    arr = {'a': 1, 'b': 2, 'c': 3}
    print('arr', arr, 'tuple', arr.items())

Tips()

#print(dir(hashlib))
#h='123456789012'
#s=':'.join(h[i:i+2] for i in range(0, 12, 2))
#print(s)

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
