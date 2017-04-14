#!/usr/bin/python

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


#CallObj(Print2, [1])
#CallObj(CallObjArr, [Print2, [1], [2]])
CallObj(CallFuncArr, ['Print2', [1], [2]])

#CallFuncArr('Print2', [1,2,3], ['a','b','c'], ['X', 'Y', 'Z'])
#OBResult = CallFuncArr(['Print3', [1, 'a', 'A'], [2, 'b', 'B'], [3, 'c', 'C'], [4, 'd', 'D']])
#Result = CallObjArr(Print2, [1], [2], [3])
#print(Result)
#Result = CallFuncArr(['Print2', [1], [2], [3]])
#print(Result)
#Result = CallFuncArr('Print1')
#print(Result)
