#---VladVons@gmail.com
# 05.02.17
# micropython ESP8266
#---

#import machine
import socket
import network
import ure
import time
import ujson
import ubinascii

from common import Log

class TWLan:
    @staticmethod
    def Scan():
        Log('TWLan.Scan')
        Result = []

        #wlan = network.WLAN(mode = network.WLAN.STA)
        nets = wlan.scan()
        for net in nets:
            Result.append(net.ssid)

        return Result

    @staticmethod
    def GetMac():
        ap_if = network.WLAN(network.AP_IF)
        mac = ap_if.config("mac")
        return ubinascii.hexlify(mac).decode("utf-8")

    @staticmethod
    def SetEssd(aName, aPassw):
        essid = "%s-%s" % (aName, TWLan.GetMac()[-4:])
        ap_if = network.WLAN(network.AP_IF)
        ap_if.config(essid = essid, authmode = network.AUTH_WPA_WPA2_PSK, password = aPassw)

    @staticmethod
    def GetInfo():
        wlan = network.WLAN(network.STA_IF)
        return wlan.ifconfig()

    @staticmethod
    def Connect(aESSID, aPassw, aTimeOut = 10000):
        Log('Connect', aESSID, aPassw)

        wlan = network.WLAN(network.STA_IF)
        Result = wlan.isconnected()
        if (not Result):
            wlan.active(True)
            wlan.connect(aESSID, aPassw)

            TimeEnd = time.ticks_ms() + aTimeOut
            while (True):
                #machine.idle()
                time.sleep_ms(250)

                Result = wlan.isconnected()
                if (Result or time.ticks_ms() > TimeEnd):
                    break

        return Result


class TServerBase:
    def __init__(self, aBind, aPort):
        Log('TserverBase.init',  aBind, aPort)

        self.Bind     = aBind
        self.Port     = aPort
        self.CallBack = None

    def __del__(self):
        self.Close()

    def Open(self):
        Log('TserverBase.Open')
        self.Sock = socket.socket()
        #self.Sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.Sock.bind( (self.Bind, self.Port) )
        #self.Sock.settimeout(10)
        self.Sock.listen(1)
        Log('Listening on', self.Bind, self.Port)

    def Close(self):
        Log('TServerBase.Close')
        if (self.Sock):
            self.Sock.close()
            self.Sock = None


class TServerJson(TServerBase):
    def __init__(self, aBind, aPort):
        TServerBase.__init__(self, aBind, aPort)
        self.BufSize = 64

    def Receive(self):
        Data = self.Conn.recv(self.BufSize)
        Log('TServerJson.Receive', Data)
        if (Data):
            return ujson.loads(Data)
        else:
            return {}

    def Send(self, aData):
        Log('TServerJson.Send', aData)
        Data = ujson.dumps( {'data': aData} )
        self.Conn.send(Data)

    def _Run(self):
        Log('TServerJson.Run')

        self.Conn, Addr = self.Sock.accept()
        Log('Client connected from', Addr)

        while (True):
            #self.Conn, Addr = self.Sock.accept()
            #Log('Client connected from', Addr)

            if (self.Active):
                DataIn = self.Receive()
                if (DataIn.get('data')):
                    if (self.CallBack):
                        DataOut = self.CallBack(self, DataIn)
                    else:
                        DataOut = 'unhandled'
                else:
                    self.Send('stop')
                    break

                self.Send(DataOut)
            else:
                break

            #self.Conn.close()
        self.Conn.close()


    def Run(self): 
        self.Open()

        self.Active = True
        while (self.Active):
            self._Run()

        self.Close()


class TServerHttp(TServerBase):
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
                            #Log('---2', Obj.group(0), Key, Value)
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
            #Log(Line)
            if (Line in (b'\r\n', b'\n', b'')):
                break
            else:
                Result.append(Line)
        return Result

    def Send(self, aData):
        #Log('TServerHttp.Send', aData)
        self.Conn.send(self.Responce(aData))

    def _Run(self):
        Log('TServer.Run')

        self.Active = True
        while (self.Active):
            Log('ready for connect')

            self.Conn, Addr = self.Sock.accept()
            if (self.Active):
                Log('client connected from', Addr)

                Data = 'Answr'
                Url = self.Parse(self.Receive())
                if (Url.get('_path')):
                    if (self.CallBack):
                        Data = self.CallBack(self, Url)

                self.Send(Data)
                self.Conn.close()

    def Run(self):
        self.Open()
        self._Run()
        self.Close()

def ServerRun(aBind = '0.0.0.0', aPort = 80):
    import socket
    print('Bind', aBind, 'Port', aPort)

    Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Sock.bind( (aBind, aPort) )
    #Sock.settimeout(5)

    while (True):
        print("waiting for data...")
        try:
            DataIn, Addr = Sock.recvfrom(128)
            DataOut = b'Server: ' + DataIn 
            SendRes = Sock.sendto(DataOut, Addr)
            #print('DataIn:', DataIn, 'DataOut:', DataOut, 'SendRes:', SendRes, 'Addr:', Addr)
        except:
            pass
