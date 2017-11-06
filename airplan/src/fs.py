#---VladVons@gmail.com
# 06.02.17
# micropython ESP8266
#---

import uos


def FileList():
    return uos.listdir()

def FileExists(aName):
    Files = FileList()
    return (aName in Files)

def FileRead(aName):
    fh = open(aName)
    Result = fh.read()
    fh.close()
    return Result
 
def FileWrite(aName, aData):
    fh = open(aName, 'w')
    Result = fh.write(aData)
    fh.close()
    return Result
