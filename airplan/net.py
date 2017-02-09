#---VladVons@gmail.com
# 05.02.17
#---

import machine
import socket
import network
import ure
import time

#------------------------------------------
class TWLan:
    def Scan(self):
        print('TWLan.Scan')
        Result = []

        #wlan = network.WLAN(mode = network.WLAN.STA)
        #nets = wlan.scan()
        #for net in nets:
        #    Result.append(net.ssid)

        return Result

    def GetInfo(self):
        wlan = network.WLAN(network.STA_IF)
        return wlan.ifconfig()

    def Connect(self, aESSID, aPassw, aTimeOut = 10000):
        print('Connect', aESSID, aPassw)

        wlan = network.WLAN(network.STA_IF)
        Result = wlan.isconnected()
        if (not Result):
            wlan.active(True)
            wlan.connect(aESSID, aPassw)

            TimeEnd = time.ticks_ms() + aTimeOut
            while (True):
                machine.idle()
                time.sleep_ms(100)

                Result = wlan.isconnected()
                if (Result or time.ticks_ms() > TimeEnd):
                    break

        return Result

#------------------------------------------
#https://www.davidgouveia.net/2016/07/controlling-relays-using-micropython-and-an-esp8266/
#https://esp8266.ru/forum/threads/micropython-http-server.1492/
class TServer:
    def __init__(self, aInterface = '0.0.0.0', aPort = 80):
        self.Interface = aInterface
        self.Port      = aPort
        self.CallBack  = None

        self.Sock = socket.socket()
        self.Sock.bind( (self.Interface, self.Port) )
        #self.Sock.settimeout(10)
        self.Sock.listen(1)
        print('Listening on', self.Interface, self.Port)
 
    def Parse(self, aRequest):
        Result = {}
        for Line in aRequest:
            print(Line)
            if ('GET ' in Line) and ('favicon.ico' not in Line):
                Obj = ure.search("GET (.*?) HTTP\/1\.1", Line)
                if (Obj):
                    Url = Obj.group(1)
                    Result['_path'] = Url
                    Result['_dir']  = ure.search("(.*?)(\?|$)", Url).group(1) 

                    while True:
                        Obj = ure.search("(\w+)=(\w+)", Url)
                        if (Obj):
                            Result[Obj.group(1)] = Obj.group(2)
                            Url = Url.replace(Obj.group(0), '')
                        else:
                            break
        return Result

    def Responce(self, aStr):
        return '''HTTP/1.0 200 OK\r\nContent-type: text/html\r\nContent-length: %d\r\n\r\n%s''' % (len(aStr), aStr)

    def Close(self):
        print('TServer.Close')

        if (self.Sock):
            self.Sock.close()
            self.Sock   = None
            self.Active = False

    def Run(self):
        print('TServer.Run')

        self.Active = True
        while (self.Active):
            print('ready for connect')
            Conn, Addr = self.Sock.accept()

            if (self.Active):
                print('client connected from', Addr)

                cl_file = Conn.makefile('rwb', 0)
                Lines = []
                while (True):
                    Line = cl_file.readline()
                    #print(Line)
                    if (not Line or Line == b'\r\n'):
                        break
                    else:
                        Lines.append(Line)

                Data = 'Answer'
                Url = self.Parse(Lines)
                if (Url.get('_path')):
                    if (self.CallBack):
                        Data = self.CallBack(self, Url)

                Conn.send(self.Responce(Data))
                Conn.close()

        self.Close()
