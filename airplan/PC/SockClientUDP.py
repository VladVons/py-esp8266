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


    def Show(self):
        print(self.Data)

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

    def MotorsClear(self):
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
        SC.SetPinsInv([cLed_Red, cLed_Green, cLed_Blue])
        #SC.Add({"Name": "Sleep", "Value": 200})
        SC.Add({"Name": "GetTicks"})
        SC.Add({"Name": "GetMemFree"})

        SC.Send(1)

def TestMotor(aPins, aForward, aSpeed):
    SC = TSockClientUDP(cHost, cPort)

    PinA = aPins[int(aForward)]
    PinB = aPins[int(not aForward)]

    if (aSpeed > 0):
        SC.SetPwmOff(PinB)
        SC.SetPwm(PinA, 300, aSpeed)
        SC.SetPin(PinB, 0)
        SC.SetPin(PinA, 1)
    else:
        SC.SetPwmOff(PinA)
        SC.SetPwmOff(PinB)
        SC.SetPin(PinA, 1)
        SC.SetPin(PinB, 1)

    #SC.Show()
    SC.Send()


TestMotor([cMotor_Nor1_Fwd, cMotor_Nor1_Rev], True, 0)
#TestLed()
 