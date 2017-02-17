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

    def UDP_1(self):
        Host = '192.168.2.144'
        Port = 80
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.settimeout(0.2)

        TimeOuts = 0
        for i in range(1, self.Count):
            DataOut = 'Packet %d ' % (i)
            sock.sendto(DataOut, (Host, Port))
            try:
                DataIn = sock.recvfrom(128)
                Duration = round((time.time() - self.Start), 2)
                print('TimeOuts', TimeOuts, "Packet", i, "Sec", Duration, "Tick", round(Duration / i, 3))
            except:
                print('Timeout')
                TimeOuts += 1


    def UDP_2(self):
        Host = '192.168.2.144'
        Port = 80
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(0.2)

        TimeOuts = 0
        for i in range(1, self.Count):
            Data = 'Packet %d ' % (i)
            DataOut = json.dumps( {"data": Data} )
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
            print('TimeOuts', TimeOuts, "Packet", i, "Sec", Duration, "Tick", round(Duration / i, 3))


ST = TSpeedTest()

#ST.Count = 1000000
#ST.Test('Concat_1')
#ST.Test('Concat_2')
#ST.Test('List_1')
#ST.Test('List_2')

ST.Count = 10
ST.Test('UDP_2')
#threads 1 ('TimeOuts', 69, 'Packet', 9999, 'Sec', 78.93, 'Tick', 0.008)
#threads 2 'TimeOuts', 85, 'Packet', 9999, 'Sec', 111.68, 'Tick', 0.011)
