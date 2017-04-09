#!/usr/bin/python

import socket
import json
import datetime


class TSocketServerUDP():
    def __init__(self, aHost, aPort):
        self.Host = aHost
        self.Port = aPort
        self.BufSize = 512

        self.Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.Sock.bind( (aHost, aPort) )
        print('Date', datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'), 'Bind', aHost, aPort)
        
    def Receive(self):
        Result = self.Sock.recvfrom(self.BufSize)
        print('Receive()', Result) 
        return Result

    def Send(self, aData, aAddr):
        print('Send()', aData, aAddr) 
        return self.Sock.sendto(aData, aAddr)
            
    def Listen(self):
        while (True):
            Data, Addr = self.Receive()
            if (Data):
                try:
                    DataIn =  json.loads(Data.decode("utf-8"))
                except:
                    DataIn = {}
            else:
                DataIn = {}

            DataIn['Ret'] = 'Returned'
    
            DataOut = json.dumps(DataIn)
            print('DataOut', DataOut) 
            self.Send(DataOut, Addr)

        self.Sock.close()

SocketServerUDP = TSocketServerUDP('0.0.0.0',  51015)
SocketServerUDP.Listen()
