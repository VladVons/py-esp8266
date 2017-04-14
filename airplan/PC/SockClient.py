#!/usr/bin/python
#--------------------
# VladVons@gmail.com
# 2017.03.25
# Ver 1.01
#--------------------

import time
import socket
import json

#

Host = '192.168.2.119'

cPinLedSys   = 2
cPinLedRed   = 15
cPinLedGreen = 12
cPinLedBlue  = 13

ArrPwm    = [0,2,4,5,12,13,14,15]
ArrPin    = [0,1,2,3,4,5,12,13,14,15,16]
#ArrLed    = [cLed_Sys, cLed_Red, cLed_Green, cLed_Blue]
ArrMotor1 = [12, 13]
ArrMotor2 = [14, 15]

#-----------

def Dump(aValue, aPref = ''):
    if (isinstance(aValue, dict)):
        for Key in aValue:
            Dump(aValue[Key], aPref + '/' + Key)
    elif (isinstance(aValue, list)):
        for Value in aValue:
            Dump(Value, aPref)
    else:
        print(aPref, aValue)


class TSerial():
    def __init__(self):
        self.Clear()

    def Show(self):
        print(self.Data)

    def Clear(self):
        self.Data = {}
        self.AddKey('Data', [])

    def GetDic(self):
        return self.Data

    def AddData(self, aData):
        self.Data['Data'].append(aData)

    def AddKey(self, aKey, aValue):
        self.Data[aKey] = aValue

    def AddFunc(self, aName, aArgs = []):
        self.AddData( {"Func": aName, "Args": aArgs} )

    def Print(self, aValue):
        return
        self.AddFunc("Log", [1, aValue])

    def Exec(self, aValue):
        self.AddFunc("Exec", [aValue])

    def SetLogLevel(self, aValue):
        self.AddFunc("SetLogLevel", [aValue])

    #--- Pin functions

    def GetPin(self, aPin):
        self.AddFunc("GetPin", [aPin])

    def SetPin(self, aPin, aValue):
        self.AddFunc("SetPin", [aPin, aValue])

    def SetPinInv(self, aPin):
        self.AddFunc("SetPinInv", [aPin])

    def GetPwmDuty(self, aPin):
        self.AddFunc("GetPwmDuty", [aPin])

    def SetPwm(self, aPin, aFreq, aDuty):
        self.AddFunc("SetPwmFreq", [aPin, aFreq])
        self.AddFunc("SetPwmDuty", [aPin, aDuty])

    def SetPwmOff(self, aPin):
        self.AddFunc("SetPwmOff", [aPin])

    def GetAdc(self):
        self.AddFunc("GetAdc")

    def AddFuncArr(self, *aArgs):
        self.AddFunc('CallFuncArr', aArgs)


class TSockClientBase():
    def __init__(self, aHost, aPort):
        self.Host  = aHost
        self.Port  = aPort

        self.Start    = time.time()
        self.SendCnt  = 0
        self.TimeOut  = 0
        self.MaxTries = 1
        self.BufSize  = 1024


    def __del__(self):
        TotalSec = round(time.time() - self.Start, 2)
        if (self.SendCnt > 0 and TotalSec > 0):
            Avg = TotalSec /  self.SendCnt
            print('')
            print("TotalSec", TotalSec, 
              "Avg", round(Avg, 3),
              "PerSec", round(1 / Avg, 3),
              "SendCnt", self.SendCnt, 
              "TimeOut", self.TimeOut)

    def Exec(self, aData, aTimeOut):
        raise NotImplementedError('abstract')

    def Print(self, aData):
        Data = aData.get('Data')
        for Item in Data:
            print(Item)

    def Send(self, aData, aTimeOut = 0.2):
        self.SendCnt += 1

        #print('Send()', 'aData', aData)  
        DataOut = json.dumps(aData) 
        print('')
        print('--- DataOut len', len(DataOut), 'SendCnt', self.SendCnt, 'TimeOut', self.TimeOut)
        self.Print(aData)

        Tries  = self.MaxTries
        DataIn = None
        while (DataIn == None and Tries > 0):
            Tries  -= 1
            DataIn = self.Exec(DataOut, aTimeOut)

        if (DataIn):
            #print('Send()', 'DataIn', DataIn)  
            Result = json.loads(DataIn)
            print('--- DataIn len', len(DataIn))
            self.Print(Result)
        else:
            Result = {}

        #Dump(Result)
        return Result


class TSockClientUDP(TSockClientBase):
    def Exec(self, aData, aTimeOut):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(aTimeOut)
        sock.sendto(aData, (self.Host, self.Port))
        try:
            Data = sock.recvfrom(self.BufSize)
            Result = Data[0]
        except:
            Result = None
            self.TimeOut += 1
            print('Timeout', self.TimeOut)
        return Result

class TSockClientTCP(TSockClientBase):
    def Exec(self, aData, aTimeOut):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(aTimeOut)
        try:
            sock.connect( (self.Host, self.Port) )
            sock.sendall(aData)
            Result = sock.recv(self.BufSize)
        except:
            Result = None
        return Result


#-----------

class TEsp():
    def __init__(self, aHost, aPort):
        self.Sock   = TSockClientUDP(aHost, aPort)
        #self.Sock   = TSockClientTCP(aHost, aPort)

        self.Serial = TSerial()

    def SetLogLevel(self, aValue):
        self.Serial.SetLogLevel(aValue)

    def Send(self, aTimeOut = 0.25):
        self.Serial.Print("--- " + str(self.Sock.SendCnt))
        Data = self.Serial.GetDic()
        Result = self.Sock.Send(Data, aTimeOut)
        self.Serial.Clear()
        return Result

    def GetInfo(self):
        self.Serial.AddFunc("GetInfo")
        #self.Serial.AddFunc("SetBufSize", [700])
        #self.Serial.AddFunc("GetTicks")
        #self.Serial.AddFunc("GetMemFree")
        #self.Serial.AddFunc("GetMachineId")
        #self.Serial.Show()

        #self.Serial.AddFunc('GetMethods', ['uos'])
        #self.Serial.AddFunc('GetMethods', ['urandom'])
        #self.Serial.AddFunc('GetMethods', ['machine'])

        self.Send()

    def GetPinInfo(self, aPins) :
        for Pin in aPins:
            self.Serial.GetPin(Pin)
            self.Serial.GetPwmDuty(Pin)
            self.Send()

    def LedFlash(self, aCnt):
        for i in range(aCnt):   
            On = i % 2
            #self.Serial.SetPin(cPinLedRed, i % 2)

            self.Serial.AddFuncArr('SetPin', [cPinLedRed, On], [cPinLedGreen, On], [cPinLedBlue, On], [cPinLedSys, On])
            #self.Serial.SetPin(cPinLedRed, On)
            #self.Serial.SetPin(cPinLedGreen, On)
            #self.Serial.SetPin(cPinLedBlue, On)
            #self.Serial.SetPin(cPinLedSys, On)

            #self.Serial.AddFunc("Sleep", [50])
            self.Send()

    def MotorDCStop(self, aPins):
        self.Serial.SetPwmOffArr(aPins)
        self.Serial.SetPinArr(aPins, 1)
        self.Send()

    def MotorDC(self, aPins, aSpeed):
        Forward = aSpeed > 0
        PinA = aPins[int(Forward)]
        PinB = aPins[int(not Forward)]

        if (aSpeed == 0):
             self.MotorDCStop(aPins)
             self.Send()
        else:
            Speed = abs(aSpeed)
            if (Speed > 1000):
                Speed = 1000

            self.Serial.SetPwmOff(PinB)
            self.Serial.SetPwm(PinA, 50, Speed)
            self.Serial.SetPin(PinB, 0)
            self.Serial.SetPin(PinA, 1)
            self.Send()

    def MotorServ(self, aPin, aValue):
        print('Pin', aPin, 'Value', aValue)
        self.Serial.SetPwm(aPin, 50, aValue)
        self.Send()

    def Exec(self, aScript, aTimeOut = 0.2):
        self.Serial.Exec(aScript)
        self.Send(aTimeOut)

    def SendFile(self, aFile):
        fh = open(aFile)
        Data = fh.read()
        fh.close()

        self.Serial.AddFunc("FileWrite", [aFile, Data])
        self.Send(2)

    def WlanSTA(self, aEssId, aPassw):
        self.Serial.AddFunc("WlanSTA", [aEssId, aPassw])
        self.Send(3)
        
#-----------

def MotorDC(aSpeed):
    Esp = TEsp(Host, 51015)
    Esp.MotorDC(ArrMotor1, aSpeed)
    Esp.MotorDC(ArrMotor2, aSpeed)

def MotorServ(aValue):
    #(27-127-77-50) (25-115-70-44)
    MotorMin = 26
    MotorMax = 114

    ValueMin = -10
    ValueMax = 10
    aValue = min(ValueMax, max(ValueMin, aValue))

    Ratio = float(MotorMax - MotorMin) / float(ValueMax - ValueMin)
    Value = MotorMin + ((aValue - ValueMin) * Ratio)       

    aPin = 5
    Esp = TEsp(Host, 51015)
    Esp.MotorServ(aPin, int(Value))

def LedFlash(aCnt, aLogLevel = 1):
    Esp = TEsp(Host, 51015)
    Esp.SetLogLevel(aLogLevel)
    #Esp.MotorDCStop(ArrMotor1)
    Esp.LedFlash(aCnt)

def Exec():
    Esp = TEsp(Host, 51015)
    Esp.Exec("SetPinInv(15);Sleep(200);SetPinInv(15);Sleep(200);SetPinInv(15)", 1)
    Esp.Exec("import esp; Result = dir(esp)")

def Call():
    Esp = TEsp(Host, 51015)
    Esp.Serial.AddFunc("GetInfo", [])
    Esp.Send()

def GetInfo():
    Esp = TEsp(Host, 51015)
    Esp.GetInfo()
    #Esp.GetPinInfo(ArrLed)

def SendFile(aFile):
    Esp = TEsp(Host, 51015)
    Esp.SetLogLevel(2)
    Esp.SendFile(aFile)

def WlanSTA(aEssId, aPassw):
    Esp = TEsp(Host, 51015)
    Esp.WlanSTA(aEssId, aPassw)


#LedFlash(101, 1)
#MotorDC(100)
#MotorServ(0)
#Exec()
#Call()
GetInfo()
#SendFile('Test.txt')
#ConnectWlan('R3-0976646510', '197119822007')


