#---VladVons@gmail.com  
# 05.02.17
# micropython ESP8266
#---

import socket
import ujson
import ubinascii
#
import log


class TSockServer():
    def __init__(self, aBind, aPort, aTimeOut):
        self.BufSize  = 512
        self.Handler  = None
        
        self._SockCreate()

        if (aTimeOut >= 0):
            self.Sock.settimeout(aTimeOut)
            #self.Sock.setblocking(False)
        self.Sock.bind( (aBind, aPort) )

    def __del__(self):
        self.Close()

    def Close(self):
        if (self.Sock):
            self.Sock.close()
            self.Sock = None

    def Run(self):
        #log.Log(3, 'Run()')

        self.Active = True
        while (self.Active):
            Data = self.Receive()
            if (self.Handler):
                Data = self.Handler(self, Data)
            if (Data):
                #log.Log(3, 'Run()', Data)
                self.Send(Data)
        self.Close()

    def SetBufSize(self, aValue):
        self.BufSize = aValue
        return aValue


class TSockJson():
    def _Receive(self):
        raise NotImplementedError('abstract')

    def _Send(self):
        raise NotImplementedError('abstract')

    def Receive(self):
        Result = {}

        Data = self._Receive()
        if (Data):
            try:
                Result = ujson.loads(Data.decode("utf-8"))
            except Exception as e:
                Error = "TSockJson.Receive() " + str(e)
                log.Log(0, Error)

                Result = {"Error": Error}
        return Result

    def Send(self, aData):
        try:
            #aData['IP'] = self.Addr
            Data = ujson.dumps(aData)
        except Exception as e:
            Data = '{"Error": "TSockJson.Send() %s"}' % e
            log.Log(0, Data)

        self._Send(Data)


class TSockServerUdpJson(TSockServer, TSockJson):
    def __init__(self, aBind, aPort, aTimeOut = -1):
        #log.Log(3, 'TServerUDPJson()', aBind, aPort)
        TSockServer.__init__(self,  aBind, aPort, aTimeOut)

    def _SockCreate(self):
        self.Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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
            self.Addr = None


class TSockServerTCPJson(TSockServer, TSockJson):
    def __init__(self, aBind, aPort, aTimeOut = -1):
        #log.Log(3, 'TServerTCPJson()', aBind, aPort)

        # prevent hard reset on  _Receive() ???
        if (aTimeOut == 0):
            aTimeOut = -1  
 
        TServerBase.__init__(self,  aBind, aPort, aTimeOut)
        self.Sock.listen(1)

    def _SockCreate(self):
        self.Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _Receive(self):
        try:
            self.Conn, self.Addr = self.Sock.accept()
            Result = self.Conn.recv(self.BufSize)
        except: 
            self.Conn = None
            Result    = None
        return Result

    def _Send(self, aData):
        if (self.Conn):
            self.Conn.sendall(aData)
            self.Conn.close()
            self.Conn = None
