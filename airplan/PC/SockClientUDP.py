#!/usr/bin/python
#--------------------
# VladVons@gmail.com
# 2017.03.25
# Ver 1.01
#--------------------

import time
import socket
import json


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

class TSockClientUDP():
    def __init__(self, aHost, aPort):
        self.Host  = aHost
        self.Port  = aPort

        self.Start    = time.time()
        self.SendCnt  = 0
        self.TimeOut  = 0
        self.MaxTries = 3
        self.Clear()

    def __del__(self):
        TotalSec = round(time.time() - self.Start, 2)
        if (self.SendCnt > 0):
            print("TotalSec", TotalSec, 
              "Avg", round(TotalSec /  self.SendCnt, 3),
              "SendCnt", self.SendCnt, 
              "TimeOut", self.TimeOut)

    def Clear(self):
        self.Data = []

    def Add(self, aData):
        self.Data.append(aData)

    def Send(self, aTimeOut = 0.2):
        self.SendCnt += 1
        self.Print("--- " +  str(self.SendCnt))

        DataOut = json.dumps(self.Data) 
        self.Clear()
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


    def Show(self):
        print(self.Data)

    def Print(self, aValue):
        self.Add({"Name": "Print", "Value": aValue})

    def Exec(self, aValue):
        self.Add({"Name": "Exec", "Value": aValue})

    #--- Pin functions

    def GetPin(self, aPin):
        self.Add({"Name": "GetPin", "Item": aPin})

    def SetPin(self, aPin, aValue):
        self.Add({"Name": "SetPin", "Item": aPin, "Value": aValue})

    def SetPinInv(self, aPin):
        self.Add({"Name": "SetPinInv", "Item": aPin})

    def GetPwm(self, aPin):
        self.Add({"Name": "GetPwm", "Item": aPin})

    def SetPwm(self, aPin, aFreq, aDuty):
        self.Add({"Name": "SetPwmFreq", "Item": aPin, "Value": aFreq})
        self.Add({"Name": "SetPwmDuty", "Item": aPin, "Value": aDuty})

    def SetPwmOff(self, aPin):
        self.Add({"Name": "SetPwmOff", "Item": aPin})

    def SetLeds(self, aValue):
        self.SetPins([cLed_Sys, cLed_Red, cLed_Green, cLed_Blue],  aValue)

    def GetAdc(self):
        self.Add({"Name":"GetAdc"})

    #--- Pin array functions

    def GetPins(self, aPins):
        self.Add({"Name": "GetPins", "Item": aPins})

    def SetPins(self, aPins, aValue):
        self.Add({"Name": "SetPins", "Item": aPins, "Value": aValue})

    def SetPinsInv(self, aPins):
        self.Add({"Name": "SetPinsInv", "Item": aPins})

    def GetPwms(self, aPins):
        self.Add({"Name": "GetPwms", "Item": aPins})

    def SetPwmsOff(self, aPins):
        self.Add({"Name": "SetPwmsOff", "Item": aPins})

#-----------

class TEsp():
    def __init__(self, aHost, aPort):
        self.SC = TSockClientUDP(aHost, aPort)

    def GetInfo(self):
        self.SC.Clear()
        self.SC.Add({"Name": "GetInfo"})
        self.SC.Add({"Name": "GetTicks"})
        self.SC.Add({"Name": "GetMemFree"})
        #self.SC.Add({"Name": "GetMachineId"})

        #self.SC.Show()
        self.SC.Send()

    def LedFlash(self, aCnt):
        self.SC.Clear()
        for i in range(aCnt):
            self.SC.SetPinsInv([cLed_Red, cLed_Green, cLed_Blue])
            #self.SC.Add({"Name": "Sleep", "Value": 50})
            self.SC.Send(0.2)

    def MotorStop(self, aPins):
        self.SC.Clear()
        self.SC.SetPwmsOff(aPins)
        self.SC.SetPins(aPins, 1)
        self.SC.Send()

    def Motor(self, aPins, aSpeed):
        self.SC.Clear()

        Forward = aSpeed > 0
        PinA = aPins[int(Forward)]
        PinB = aPins[int(not Forward)]

        if (aSpeed == 0):
             self.MotorStop(Pins)
             self.SC.Send()
        else:
            Speed = abs(aSpeed)
            if (Speed > 1000):
                Speed = 1000

            self.SC.SetPwmOff(PinB)
            self.SC.SetPwm(PinA, 100, Speed)
            self.SC.SetPin(PinB, 0)
            self.SC.SetPin(PinA, 1)
            self.SC.Send()

    def Exec(self, aScript):
        self.SC.Exec(aScript)
        self.SC.Send()

#-----------

def Test1():
    Esp = TEsp("192.168.2.144", 51015)

    Esp.GetInfo()

    Esp.MotorStop(ArrMotor1)
    Esp.LedFlash(1000)

    Esp.Motor(ArrMotor1, -200)

def Test2():
    Esp = TEsp("192.168.2.144", 51015)
    Esp.Exec("Result = SetPinInv(15)")
    Esp.GetInfo()


#Test1()
Test2()
