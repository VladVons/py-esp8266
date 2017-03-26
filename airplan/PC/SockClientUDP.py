#!/usr/bin/python

import time
import socket
import json


cHost = "192.168.2.144"
cPort = 51015

ArrPwm = [0,2,4,5,12,13,14,15]
ArrPin = [0,1,2,3,4,5,12,13,14,15,16]

cMotor_Nor1_Fwd = 13
cMotor_Nor1_Rev = 12
cMotor_Nor2_Fwd = 14
cMotor_Nor2_Rev = 16

cLed_Sys   = 2
cLed_Red   = 15
cLed_Green = 12
cLed_Blue  = 13


class TSockClientUDP():
    def __init__(self, aHost, aPort):
        self.Host  = aHost
        self.Port  = aPort

        self.Start = time.time()
        self.Count = 0
        self.Delay = 0.1
        self.Clear()

    #def __del__(self):
    #    print("Total sec", round(time.time() - self.Start, 2))

    def Clear(self):
        self.Data = []

    def Add(self, aData):
        self.Data.append(aData)

    def Send(self, aTimeOut = 0.2):
        self.Count += 1
        self.Print("--- " +  str(self.Count))

        DataOut = json.dumps(self.Data) 
        self.Clear()
        print("DataOut Len", len(DataOut),  DataOut)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(aTimeOut)
        sock.sendto(DataOut, (self.Host, self.Port))
        try:
            DataIn = sock.recvfrom(1024)
            print("")
            print("DataIn len", len(DataIn[0]), DataIn)
        except:
            print('Timeout')
            DataIn = None

        if (DataIn):
            Result = json.loads(DataIn[0])
        else:
            Result = {}
        return Result

    def Print(self, aValue):
        self.Add({"Name": "Print", "Value": aValue})

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

    def Motorslear(self):
        self.SetPins([cMotor_Nor1_Fwd, cMotor_Nor1_Rev, cMotor_Nor2_Fwd, cMotor_Nor2_Rev], 0)

    def GetAdc(self):
        self.Add({"Name":"GetAdc"})

    #---

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



def TestLed():
    SC = TSockClientUDP(cHost, cPort)
    for i in range(100):
        #SC.SetPins([cLed_Red, cLed_Green, cLed_Blue], 1)
        SC.SetPinsInv([cLed_Red, cLed_Green, cLed_Blue])
        #SC.Add({"Name": "Sleep", "Value": 300})
        #SC.Add({"Name": "GetTicks"})

        #SC.SetPins([cLed_Red, cLed_Green, cLed_Blue], 0)
        #SC.Add({"Name": "Sleep", "Value": 300})

        #SC.Add({"Name": "GetMemFree"})

        SC.Send(1)

def TestMotor():
    SC = TSockClientUDP(cHost, cPort)

    #SC.GetAdc()
    #SC.GetPins(ArrPin)
    #SC.GetPwms(ArrPwm)
    #SC.SetPins(ArrPin, 0)

    SC.Motorslear()
    SC.SetPin(cMotor_Nor1_Fwd, 0)
    SC.SetPin(cMotor_Nor1_Rev, 0)

    SC.SetPwm(cMotor_Nor1_Fwd, 1023, 100)
    SC.Send(1)

def Test1():
    SC = TSockClientUDP(cHost, cPort)

    #SC.SetPins(ArrPin, 0)
    #SC.SetPins([cLed_Green], 0)
    #SC.SetPwms([12], 200, 300)
    #SC.Add({"Name": "GetMemFree"})

    #for Pin in ArrPwm:
    #    SC.SetPin(Pin, 0)
    #    SC.SetPwm(Pin, 30, 1000)
    #    SC.Send()
 
    #SC.SetPin(12, 0)
    #SC.SetPwm(12, 500, 900)
    #SC.SetPwmOff(12)
    #SC.Send()

    SC.SetPwmsOff(ArrPwm)
    SC.SetPins(ArrPwm, 0)

    SC.GetPwms(ArrPwm)
    SC.Send()



#TestMotor()
TestLed()
#Test1()
 