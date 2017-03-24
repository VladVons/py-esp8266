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
    def __init__(self, aBind, aPort):
        self.Handler = None
        self.BufSize = 128

        self.Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.Sock.bind( (aBind, aPort) )

    def __del__(self):
        self.Close()

    def Close(self):
        if (self.Sock):
            self.Sock.close()
            self.Sock = None

    def _Receive(self):
        Result, self.Addr = self.Sock.recvfrom(self.BufSize)
        return Result

    def _Send(self, aData):
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
                #print('TServerUdpBase', Data)
                if (self.Handler):
                    Data = self.Handler(self, Data)
                self.Send(Data)


class TServerUdpJson(TServerUdpBase):
    def __init__(self, aBind, aPort):
        TServerUdpBase.__init__(self, aBind, aPort)

    def Receive(self):
        Result = {}

        Data = self._Receive()
        if (Data):
            try:
                Result = ujson.loads(Data.decode("utf-8"))
            except:
                pass

        return Result

    def Send(self, aData):
        try:
            Data = ujson.dumps(aData)
        except:
            Data = '{"exception":"json"}'

        self._Send(Data)
