#---VladVons@gmail.com
# 05.02.17
# micropython ESP8266
#---

import socket
import ujson
import ubinascii
#
#from common import Log

class TServerUdpBase():
    def __init__(self, aBind, aPort, aTimeOut = -1):
        self.Handler = None
        self.BufSize = 512

        self.Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        if (aTimeOut != -1):
            self.Sock.settimeout(aTimeOut)
        self.Sock.bind( (aBind, aPort) )

    def __del__(self):
        self.Close()

    def Close(self):
        if (self.Sock):
            self.Sock.close()
            self.Sock = None

    def _Receive(self):
        try:
            Result, self.Addr = self.Sock.recvfrom(self.BufSize)
        except OSError:
            self.Addr = None
            Result    = None
        return Result

    def _Send(self, aData):
        if (self.Addr):
            self.Sock.sendto(aData, self.Addr)

    def Receive(self):
        return self._Receive()

    def Send(self, aData):
        self._Send()

    def Run(self):
        self.Active = True
        while (self.Active):
            if (self.Active):
                Data = self.Receive()
                if (self.Handler):
                    Data = self.Handler(self, Data)
                self.Send(Data)


class TServerUdpJson(TServerUdpBase):
    def __init__(self, aBind, aPort, aTimeOut = -1):
        TServerUdpBase.__init__(self, aBind, aPort, aTimeOut)

    def Receive(self):
        Result = {}

        Data = self._Receive()
        if (Data):
            try:
                Result = ujson.loads(Data.decode("utf-8"))
            except:
                Data = '{"exception": "Receive() json"}'

        return Result

    def Send(self, aData):
        try:
            aData['IP'] = self.Addr
            Data = ujson.dumps(aData)
        except:
            Data = '{"exception": "Send() json"}'

        self._Send(Data)
