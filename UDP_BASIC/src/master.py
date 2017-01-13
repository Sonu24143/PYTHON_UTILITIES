#!/usr/bin/python
#MASTER

import socket
from sys import argv
import thread
import os
import pool


CONN_REQ="CONNECTION_REQUEST"
MSG_TXT="MESSAGE_TEXT"
DSCNCT_TXT="DISCONNNECT_REQUEST"
MESSAGE_SIZE=2048
connection_pool=pool.Pool()
SEND_SOCKET=socket.socket( socket.AF_INET , socket.SOCK_DGRAM )

def createConnection(m,a):
        addr=(a[0],int(m[0]))
	print m
	print addr
        r=connection_pool.addToPool(str(m[1]),addr)
	connection_pool.getData()
        if(r==0):
                SEND_SOCKET.sendto("RESPONSE:SUCCESS",addr)
        else:
                SEND_SOCKET.sendto("RESPONSE:FAILURE",addr)

def getUsers(n):
        connection_pool.getAvailableConnections(n)

def sendIt(m):
        n=str(m[0])
        msg=m[1]+": "+" ".join(m[2:])
        if ( m[2] == "GETUSERS" ):
                getUsers(n)
        else:
                connection_pool.sendMessageTo(n,msg)
                return 0

def destroyConnection(m):
        r=connection_pool.removeFromPool(m.strip(" "))
	connection_pool.getData()
        return r


def process(msg,addr):
	print msg
        if( msg.split(":")[0] == CONN_REQ ):
                return_code=createConnection(msg.split(":")[1:],addr)
                if ( return_code == 0 ):
                        return 0
                else:
                        return 1

        elif( msg.split(":")[0] == MSG_TXT ):
                return_code=sendIt(msg.split(":")[1:])
                if ( return_code == 0 ):
                        return 0
                else:
                        return 1

        elif(msg.split(":")[0] == DSCNCT_TXT):
                return_code=destroyConnection(msg.split(":")[1])
                if ( return_code == 0 ):
                        return 0
                else:
                        return 1

        else:
                return 1


def listener( s , a ):
        s.bind(a)
        print("Listening on "+a[0]+":"+str(a[1]))
        while True:
                msg , addr = s.recvfrom( MESSAGE_SIZE )
                process(msg,addr)

def Main():
        if len(argv) != 3:
                print("Please use the right format ./master.py listen_ip listen_port")
                exit(1)
        HOST_IP=argv[1]
        IN_PORT=int(argv[2])
        LISTEN_SOCKET = socket.socket( socket.AF_INET , socket.SOCK_DGRAM )
        LOCAL_ADDRESS = ( HOST_IP , IN_PORT )
        listener(LISTEN_SOCKET,LOCAL_ADDRESS)
#       try:
#               thread.start_new_thread( listener , (UDP_SERVER_LISTEN,LOCAL_ADDRESS,) )
#       except Exception as errtxt:
#               print errtxt

#       message=""
#       print("########## CHATBOT ##########")
#       while True:
#               message=raw_input()
#               UDP_CLIENT_SENDER.sendto(message,GUEST_ADDRESS)
#               if ( message == "bye" or message == "Bye" or message == "BYE" ):
#                       break
        exit(0)

if __name__ == "__main__":
        Main()

