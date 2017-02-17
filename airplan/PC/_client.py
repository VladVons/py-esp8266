#!/usr/bin/python

#---VladVons@gmail.com
# 12.02.17
# python for PC 
#---


import urllib2
import time
import socket
import json


def TestHttp():
    for i in range(1000):
        Led1 = int(i % 2 == 0)
        Str1 = "http://192.168.2.144/led?on=%d&try=%d" % (Led1, i)
        print(i, Str1)
        urllib2.urlopen(Str1).read()
        time.sleep(0.1)


class TSockClient():
    def __init__(self, aHost, aPort):
        self.Host      = aHost
        self.Port      = aPort
        self.BufSize   = 512
        self.Sock      = None

    def Open(self):
        self.Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Sock.connect( (self.Host, self.Port) )

    def Send(self, aData):
        Data = json.dumps( {"data": aData} )
        self.Sock.send(Data)
        return self.ReceiveData()

    def Receive(self):
        return self.Sock.recv(self.BufSize)

    def ReceiveData(self):
        Data = self.Receive()
        if (Data):
            return json.loads(Data).get("data")
        else:
            return ''

    def Close(self):
        if (self.Sock):
            self.Sock.close()
            self.Sock = None


def TestSpeed1(aCount):
    #SockClient = TSockClient('192.168.4.1',   80)
    SockClient = TSockClient('192.168.2.144', 80)
    SockClient.Open()

    Start = time.time()
    for i in range(1, aCount):
        #SockClient.Open()

        Data = SockClient.Send('Data %i' % (i))
        Duration = round((time.time() - Start), 2) 
        print("Data", Data, "Sec", Duration, "Tick", round(Duration / i, 2))

        #SockClient.Close()
        #time.sleep(0.1)

def Client_TestSpeed(aHost, aPort = 80, aCount = 1000):
    import socket

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(0.2)

    TimeOuts = 0
    Start = time.time()
    for i in range(1, aCount):
        DataOut = 'Packet %d ' % (i)
        sock.sendto(DataOut, (aHost, aPort))
        #print("Sent", DataOut)

        try:
            DataIn = sock.recvfrom(128)
            #print("DataIn", DataIn)
            Duration = round((time.time() - Start), 2) 
            print('TimeOuts', TimeOuts, "Packet", i, "Sec", Duration, "Tick", round(Duration / i, 3))
        except:
            print('Timeout')
            TimeOuts += 1

        #time.sleep(0.1)

#Client_TestSpeed('192.168.2.144', 80, 1000)
