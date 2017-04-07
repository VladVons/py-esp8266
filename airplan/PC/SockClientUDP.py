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
import Test


cLed_Sys   = 2
cLed_Red   = 15
cLed_Green = 12
cLed_Blue  = 13

ArrPwm    = [0,2,4,5,12,13,14,15]
ArrPin    = [0,1,2,3,4,5,12,13,14,15,16]
ArrLed    = [cLed_Sys, cLed_Red, cLed_Green, cLed_Blue]
ArrMotor1 = [13, 12]
ArrMotor2 = [14, 16]

#-----------

class TSerial():
    def __init__(self):
        self.Clear()

    def Clear(self):
        self.Data = {'Data': []}

    def GetData(self):
        return self.Data

    def Add(self, aData):
        self.Data['Data'].append(aData)

    def Show(self):
        print(self.Data)

    def AddFunc(self, aName, aArgs = []):
        self.Add({"ID": "myTSerial", "Func": aName, "Args": aArgs})

    def Print(self, aValue):
        self.AddFunc("Print", [aValue])

    def Exec(self, aValue):
        self.AddFunc("Exec", ["Result = " + aValue])

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

    def SetLeds(self, aValue):
        self.SetPins([cLed_Sys, cLed_Red, cLed_Green, cLed_Blue],  aValue)

    def GetAdc(self):
        self.AddFunc("GetAdc")

    #--- Pin array functions

    def GetPinArr(self, aPins):
        self.AddFunc("GetPinArr", [aPins])

    def SetPinArr(self, aPins, aValue):
        self.AddFunc("SetPinArr", [aPins, aValue])

    def SetPinInvArr(self, aPins):
        self.AddFunc("SetPinInvArr", [aPins])

    def GetPwmArr(self, aPins):
        self.AddFunc("GetPwmArr", [aPins])

    def SetPwmOffArr(self, aPins):
        self.AddFunc("SetPwmOffArr", [aPins])



class TSockClientUDP():
    def __init__(self, aHost, aPort):
        self.Host  = aHost
        self.Port  = aPort

        self.Start    = time.time()
        self.SendCnt  = 0
        self.TimeOut  = 0
        self.MaxTries = 3

    def __del__(self):
        TotalSec = round(time.time() - self.Start, 2)
        if (self.SendCnt > 0):
            Avg = TotalSec /  self.SendCnt
            print("TotalSec", TotalSec, 
              "Avg", round(Avg, 3),
              "PerSec", round(1 / Avg, 3),
              "SendCnt", self.SendCnt, 
              "TimeOut", self.TimeOut)

    def Send(self, aData, aTimeOut = 0.2):
        self.SendCnt += 1

        DataOut = json.dumps(aData) 
        print("DataOut Len", len(DataOut),  DataOut)

        Tries  = self.MaxTries
        DataIn = None
        while (DataIn == None and Tries > 0):
            Tries  -= 1

            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(aTimeOut)
            sock.sendto(DataOut, (self.Host, self.Port))
            try:
                DataIn = sock.recvfrom(1024)
                print("")
                print("DataIn len", len(DataIn[0]), DataIn)
            except:
                self.TimeOut += 1
                print('Timeout', self.TimeOut, "Tries", Tries)

        if (DataIn):
            Result = json.loads(DataIn[0])
        else:
            Result = {}
        return Result


#-----------

class TEsp():
    def __init__(self, aHost, aPort):
        self.Sock   = TSockClientUDP(aHost, aPort)
        self.Serial = TSerial()

    def Send(self, aTimeOut = 0.2):
        self.Serial.Print("--- " + str(self.Sock.SendCnt))
        self.Sock.Send(self.Serial.GetData(), aTimeOut)
        self.Serial.Clear()

    def GetInfo(self):
        self.Serial.AddFunc("GetInfo")
        self.Serial.AddFunc("GetTicks")
        self.Serial.AddFunc("GetMemFree")
        #self.Serial.AddFunc("GetMachineId")
        #self.Serial.Show()
        self.Send()

    def GetPinImfo(self, aPins) :
        for Pin in aPins:
            self.Serial.GetPin(Pin)
            self.Serial.GetPwmDuty(Pin)
            self.Send()

    def LedFlash(self, aCnt):
        for i in range(aCnt):
            self.Serial.SetPinArr([cLed_Red, cLed_Green, cLed_Blue], i % 2)
            #self.Serial.AddFunc("Sleep", [50])
            self.Send(0.2)

    def MotorStop(self, aPins):
        self.Serial.SetPwmOffArr(aPins)
        self.Serial.SetPinArr(aPins, 1)
        self.Send()

    def Motor(self, aPins, aSpeed):
        Forward = aSpeed > 0
        PinA = aPins[int(Forward)]
        PinB = aPins[int(not Forward)]

        if (aSpeed == 0):
             self.MotorStop(Pins)
             self.Send()
        else:
            Speed = abs(aSpeed)
            if (Speed > 1000):
                Speed = 1000

            self.Serial.SetPwmOff(PinB)
            self.Serial.SetPwm(PinA, 100, Speed)
            self.Serial.SetPin(PinB, 0)
            self.Serial.SetPin(PinA, 1)
            self.Send()

    def Exec(self, aScript, aTimeOut = 0.2):
        self.Serial.Exec(aScript)
        self.Send(aTimeOut)

#-----------

def TestMotor(aSpeed):
    Esp = TEsp("192.168.2.119", 51015)
    Esp.GetInfo()
    Esp.Motor(ArrMotor1, aSpeed)

def TestLamp(aCnt):
    Esp = TEsp("192.168.2.119", 51015)
    Esp.MotorStop(ArrMotor1)
    Esp.LedFlash(aCnt)

def TestExec():
    Esp = TEsp("192.168.2.119", 51015)
    Esp.Exec("SetPinInv(15);Sleep(200);SetPinInv(15);Sleep(200);SetPinInv(15)", 3)
    Esp.GetInfo()

def TestCall():
    Esp = TEsp("192.168.2.119", 51015)
    Esp.Sock.Add({"Func": "GetInfo", "Args": []})
    Esp.Sock.Send()

def TestPinInfo():
    Esp = TEsp("192.168.2.119", 51015)
    Esp.GetPinImfo(ArrLed)


TestLamp(10)
#TestMotor(-200)
#TestExec()
#TestCall()
#TestPinInfo()

#Class = globals()["Test"]
#Class.Print("Hello")
#Class.Log(2, "Hello")
#Class.CallObj("Print")

#Str = 'Pink.Floyd'
#StrA = Str.split(',')
#print(len(Str), len(StrA))

#print(('x' * 10))
