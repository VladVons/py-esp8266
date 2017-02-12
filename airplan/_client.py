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

    def Connect(self):
        if (not self.Connected()):
            self.Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self.Sock.connect( (self.Host, self.Port) )
                Data = self.Send("start")
                if (Data):
                    print(Data)
                else:
                    self.Close()
            except Exception as E:
                print(E.message)
                self.Close()
                raise

    def Connected(self):
        return (self.Sock != None)

    def Send(self, aData):
        Data = json.dumps( {"data": aData} )
        self.Sock.sendall(Data)
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
        if (self.Connected()):
            self.Sock.close()
            self.Sock = None
            print("TSockClient.Close")


def TestSpeed(aCount):
    SockClient = TSockClient('192.168.2.144', 80)
    SockClient.Connect()

    Start = time.time()
    for i in range(1, aCount):
        Data = SockClient.Send('Data %i' % (i))
        Duration = round((time.time() - Start), 2) 
        print("Data", Data, "Sec", Duration, "Tick", round(Duration / i, 2))



TestSpeed(10000)
