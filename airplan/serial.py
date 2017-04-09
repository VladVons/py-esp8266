#---VladVons@gmail.com
# 02.04.17
# micropython ESP8266
#---

import log
import api


class TSerial:
    def __init__(self):
        self.CntCall    = 0
        self.CntPacket  = 0
        self.DefUnit    = api

    def SetDefUnit(self, aName):
        self.DefUnit  = __import__(aName)

    def GetInfo(self):
        Result = 'CntPacket %d, CntCall %d' % (self.CntPacket, self.CntCall)
        print(Result)
        return Result

    def CallObj(self, aObj, aArgs):
        if (aArgs):
            ArgCnt = len(aArgs)
            if   (ArgCnt == 1):
                Result = aObj(aArgs[0])
            elif (ArgCnt == 2):
                Result = aObj(aArgs[0], aArgs[1])
            elif (ArgCnt == 3):
                Result = aObj(aArgs[0], aArgs[1], aArgs[2])
            else:
                Result = aObj()
        else:
            Result = aObj()
        return Result

    def ParseRaw(self, aData):
        aFunc  = aData.get('Func',  None)
        aArgs  = aData.get('Args',  None)

        self.CntCall += 1 
        log.Log(2, 'ParseRaw()', 'CntCall', self.CntCall, 'Func', aFunc, 'Args', aArgs)

        Result = None
        if (aFunc):
            FuncSplit = aFunc.split('.')
            try:
                if (len(FuncSplit) == 2):
                    Obj = getattr(__import__(FuncSplit[0]), FuncSplit[1])
                else:
                    Obj = getattr(self.DefUnit, aFunc)
            except:
                Obj = None

            if (Obj):
                Result = self.CallObj(Obj, aArgs)
            else:
                Result = 'Error: Unknown Func ' + aFunc
                log.Log(0, 'Parse()', Result)
        aData['Result'] = Result
        return aData

    def Parse(self, aJson):
        self.CntPacket += 1;
        log.Log(1, 'Parse()', 'CntPacket', self.CntPacket, aJson)
        
        aData  = aJson.get('Data', None)
        if (aData):
            # array of requests
            if (isinstance(aData, list)):
                Result = []
                for Data in aData:
                    Result.append(self.ParseRaw(Data))
            else:
                Result = self.ParseRaw(aData)
        else:
            Result = 'Empty Data' 

        aJson['Data'] = Result
        return aJson
