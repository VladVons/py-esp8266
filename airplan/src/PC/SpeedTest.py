#!/usr/bin/python

import time
import socket
import json

class TSpeedTest():
    def __init__(self):
        self.Start = time.time()
        self.Count = 1000000

    def __del__(self):
        print("Total sec", round(time.time() - self.Start, 2))

    def Test(self, aMethod):
        Start = time.time()
        Obj = getattr(self, aMethod)
        Obj()
        print('Method', aMethod, 'Sec', round(time.time() - Start, 2))
        
    def Concat_1(self):
        One   = "One"
        Two   = "Two"
        Three = "Three"    
        for i in range(self.Count):
            out = "<html>" + One + Two + Three + "</html>"

    def Concat_2(self):
        One   = "One"
        Two   = "Two"
        Three = "Three"    
        for i in range(self.Count):
            out = "<html>%s %s %s</html>" % (One, Two, Three)

    def List_1(self):
        Items = ['One', 'Two', 'Three'] 
        for i in range(self.Count):
            Result = ""
            for Item in Items:
                Result += Item
        return Result

    def List_2(self):
        Items = ['One', 'Two', 'Three'] 
        for i in range(self.Count):
            Result = "".join(Items)
        return Result

    def Client_UDP_1(self):
        Host = '192.168.2.144'
        #Host = '127.0.0.1'
        Port = 51015
        cMotorDC1 = 12 
        cMotorDC2 = 14

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.2)

        TimeOuts = 0
        for i in range(1, self.Count):
            Data = 'Packet %d ' % (i)
            DataOut = json.dumps( {"data": Data, "Name":"MotorDC", "No":cMotorDC1, "Value":500} )
            DataOut = json.dumps( {"data": Data, "Name":"MotorDC", "No":cMotorDC2, "Value":700} )
            sock.sendto(DataOut, (Host, Port))

            try:
                DataIn = sock.recvfrom(128)
            except:
                print('Timeout')
                TimeOuts += 1
                DataIn   = None

            if (DataIn):
                Data = json.loads(DataIn[0])
            else:
                Data = ''

            Duration = round((time.time() - self.Start), 2)
            print('TimeOuts', TimeOuts, "Packet", i, "Sec", Duration, "Tick", round(Duration / i, 3), 'Data', Data)

ST = TSpeedTest()

#ST.Count = 1000000
#ST.Test('Concat_1')
#ST.Test('Concat_2')
#ST.Test('List_1')
#ST.Test('List_2')

ST.Count = 2
ST.Test('Client_UDP_1')
#threads 1 ('TimeOuts', 69, 'Packet', 9999, 'Sec', 78.93, 'Tick', 0.008)
#threads 2 'TimeOuts', 85, 'Packet', 9999, 'Sec', 111.68, 'Tick', 0.011)

