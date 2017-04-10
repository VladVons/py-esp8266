#!/usr/bin/python

LogLevel= 3

def Log(aLevel, *aParam):
    if (aLevel <= LogLevel):
        print("LogLevel %d: %s" % (aLevel, list(aParam)))

def Print(aMsg = "Print"):
    print("Print", aMsg)
    return 10

def CallObj(aFunc):
    #Unit = globals()["Test"]
    #Obj = getattr(Unit, aFunc)
    #Obj()
    print(aFunc)
    return eval(aFunc)

print(float(7)/3)
