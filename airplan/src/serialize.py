#---VladVons@gmail.com
# 02.04.17
# micropython ESP8266
#---

import log
import api


class TSerialize:
    def __init__(self):
        self.CntCall    = 0
        self.CntPacket  = 0
        self.DefUnit    = api
        self.UserObj    = {}

    def SetDefUnit(self, aName):
        self.DefUnit  = __import__(aName)

    def AddObj(self, aName, aObj):
        try:
            #check if object exists in namespace
            aObj
            self.UserObj[aName] = aObj
        except Exception as e:
            log.Log(0, 'TSerialize.AddObj()', e)

    def CallObj(self, aObj, aArgs):
        if (aArgs):
            #Obj(aArgs[0], aArgs[1], aArgs[2])
            Result = aObj(*aArgs)  
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
                if (aFunc in self.UserObj):
                    Obj = self.UserObj[aFunc]
                else:
                    if (len(FuncSplit) == 2):
                        Obj = getattr(__import__(FuncSplit[0]), FuncSplit[1])
                    else:
                        Obj = getattr(self.DefUnit, aFunc)
            except:
                Obj = None

            if (Obj):
                Result = self.CallObj(Obj, aArgs)
            else:
                Result = 'Error: unknown Func ' + aFunc
                log.Log(0, 'TSerialize.Parse()', Result)
        else:
            Result = 'Error: empty Func'
            log.Log(0, 'TSerialize.Parse()', Result)

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
        #log.Log(3, 'Parse()', aJson)
        return aJson
