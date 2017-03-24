#!/usr/bin/python

import time
import socket
import json

class TSockClientUDP():
    cMotor_Nor1_Fwd = 13
    cMotor_Nor1_Rev = 12
    cMotor_Nor2_Fwd = 14
    cMotor_Nor2_Rev = 16

    cLed_Sys   = 2
    cLed_Red   = 15
    cLed_Green = 12
    cLed_Blue  = 13


    def __init__(self, aHost, aPort):
        self.Host  = aHost
        self.Port  = aPort

        self.Start = time.time()
        self.Count = 1000000

    #def __del__(self):
    #    print("Total sec", round(time.time() - self.Start, 2))


    def Send(self, aData):
        DataOut = json.dumps(aData) 
        print("DataOut", DataOut)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.2)
        sock.sendto(DataOut, (self.Host, self.Port))
        try:
            DataIn = sock.recvfrom(128)
        except:
            print('Timeout')
            DataIn = None

        if (DataIn):
            Result = json.loads(DataIn[0])
        else:
            Result = {}

        print("DataIn", Result)

    def GetPwm(self, aNo):
        self.Send({"Name":"GetPwm", "No":aNo})

    def SetPwm(self, aNo, aValue, aDuty):
        self.Send({"Name":"SetPwm", "No":aNo, "Value":aValue, "Duty":aDuty})

    def GetPwms(self, aPins):
        for Pin in aPins:
            self.GetPwm(Pin)
            time.sleep(0.1)

    def GetPin(self, aNo):
        self.Send({"Name":"GetPin", "No":aNo})

    def SetPin(self, aNo, aValue):
        self.Send({"Name":"SetPin", "No":aNo, "Value":aValue})

    def GetPins(self, aPins):
        for Pin in aPins:
            self.GetPin(Pin)

    def SetPins(self, aPins, aValue):
        for Pin in aPins:
            self.SetPin(Pin, aValue)
            time.sleep(0.1)

    def SetLeds(self, aValue):
        self.SetPin(self.cLed_Sys,   aValue)
        self.SetPin(self.cLed_Red,   aValue)
        self.SetPin(self.cLed_Green, aValue)
        self.SetPin(self.cLed_Blue,  aValue)

    def Motorslear(self):
        self.SetPin(self.cMotor_Nor1_Fwd, 0)
        self.SetPin(self.cMotor_Nor1_Rev, 0)
        self.SetPin(self.cMotor_Nor2_Fwd, 0)
        self.SetPin(self.cMotor_Nor2_Rev, 0)

    def GetAdc(self):
        self.Send({"Name":"GetAdc"})




SC = TSockClientUDP("192.168.2.144", 51015)

ArrPwm = [0,2,4,5,12,13,14,15]
ArrPin = [0,1,2,3,4,5,12,13,14,15,16]

SC.GetAdc()
SC.GetPins(ArrPin)
SC.GetPwms(ArrPwm)
#SC.SetPins(ArrPin, 0)

#SC.Motorslear()
#SC.SetPin(SC.cMotor_Nor1_Fwd, 0)
#SC.SetPin(SC.cMotor_Nor1_Rev, 0)

#SC.SetPin(SC.cMotor_Nor1_Fwd, 0)
#SC.SetPin(SC.cMotor_Nor1_Rev, 0)

#SC.SetPwm(SC.cMotor_Nor1_Fwd, 400, 500)
