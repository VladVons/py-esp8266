#---VladVons@gmail.com
# 05.02.17
# micropython ESP8266
#---

import socket
import ure

from common import Log


class TServerBase:
    def __init__(self, aBind, aPort):
        self.BufSize  = 512
        self.Handler  = None

        self.Sock = socket.socket()
        self.Sock.bind( (aBind, aPort) )
        self.Sock.listen(1)

    def __del__(self):
        self.Close()

    def Close(self):
        if (self.Sock):
            self.Sock.close()
            self.Sock = None

    def _Receive(self):
        return self.Conn.recv(self.BufSize)

    def _Send(self, aData):
        self.Conn.sendall(aData)

    def Run(self):
        self.Active = True
        while (self.Active):
            if (self.Active):
                self.Conn, Addr = self.Sock.accept()
                Data = self.Receive()
                if (self.Handler):
                    Data = self.Handler(self, Data)

                self.Send(Data)
                self.Conn.close()


class TServerTcpHttp(TServerBase):
    def __init__(self, aBind, aPort = 80):
        TServerBase.__init__(self, aBind, aPort)

    def Parse(self, aRequest):
        Result = {}
        for Line in aRequest:
            #print(Line)
            if ('GET ' in Line) and ('favicon.ico' not in Line):
                Obj = ure.search("GET (.*?) HTTP\/1\.1", Line)
                if (Obj):
                    Url = Obj.group(1)
                    Result['_path'] = Url
                    Result['_dir']  = ure.search("(.*?)(\?|$)", Url).group(1) 

                    while True:
                        #Obj = ure.search("(\w+)=([\w\.]+)", Url)
                        Obj = ure.search("(\w+)=([a-z0-9.]+)", Url)
                        if (Obj):
                            Key   = Obj.group(1)
                            Value = Obj.group(2)
                            Result[Key] = Value
                            Url = Url.replace(Obj.group(0), '')
                        else:
                            break
        return Result

    def Responce(self, aStr):
        aStr = aStr.replace('\n', '<br>')
        Result = (
            'HTTP/1.0 200 OK\r\n'
            'Content-type: text/html\r\n'
            'Content-length: %d\r\n'
            '\r\n'
            '%s'
            ) % (len(aStr), aStr)
        return Result
    
    def Receive(self):
        Result = []

        cl_file = self.Conn.makefile('rwb', 0)
        while (True):
            Line = cl_file.readline()
            if (Line in (b'\r\n', b'\n', b'')):
                break
            else:
                Result.append(Line)

        if (self.Handler):
            return self.Parse(Result)
        else:
            return 'Undefined handler'

    def Send(self, aData):
        self._Send(self.Responce(aData))
