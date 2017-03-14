#!/usr/bin/python

import socket
import json
import datetime

def SocketServerUDP_1():
    Host = '0.0.0.0'
    Port = 51015

    Sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    Sock.bind( (Host, Port) )
    print('Date', datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'), 'Bind', Host, Port, "Date")

    while (True):
        Data, Addr = Sock.recvfrom(512)
        print('Date', datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S'), 'Data', Data, 'Addr', Addr, 'Bind', Host, Port)

        if (Data):
            DataIn =  json.loads(Data.decode("utf-8"))
        else:
            DataIn = {}

        DataIn['Ret'] = 'Returned'
    
        Data = json.dumps(DataIn)
        Sock.sendto(Data, Addr)

    Sock.close()

SocketServerUDP_1()
