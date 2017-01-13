#!/usr/bin/python

import socket

class Pool:
        validity=[]
        names=[]
        ip_addresses=[]
        ports=[]
	

	def __init__(self):
		self.validity=[]
	        self.names=[]
	        self.ip_addresses=[]
	        self.ports=[]

	def getData(self):
		print self.validity
		print self.names
		print self.ip_addresses
		print self.ports

	def sendMessageTo( self , name , msg ):
		if( self.validity[self.names.index(name)] == 1):
			i=self.names.index(name)
			address=(self.ip_addresses[i],self.ports[i])
			SENDER_SOCKET=socket.socket(socket.AF_INET , socket.SOCK_DGRAM )
			SENDER_SOCKET.sendto(msg,address)
			SENDER_SOCKET.close()
			print("<"+name+"> "+msg)
			return 0
		else:
			print("Invalid user or user not connected anymore")
			return 1		

        def getAvailableConnections(self,name):
                temp=[]
                for n in self.names:
                        if ( self.validity[self.names.index(n)] == 1 and n != name ):
                                temp.append(n)
                self.sendMessageTo(name,"ONLINE USER's: "+str(" | ".join(temp)))

        def getFreeindex(self):
                counter=0
                for i in self.validity:
                        if i == 0:
                                return counter
                        counter+=1
                return -1

        def addToPool(self,name,address):
                n=name
                ip=address[0]
                p=int(address[1])
                for i in self.names:
                        if ( i == name and self.validity[self.names.index(name)] == 1):
                                return 1
                index=self.getFreeindex()
                if ( index == -1 ):
                        self.validity.append(1)
                        self.names.append(name)
                        self.ip_addresses.append(ip)
                        self.ports.append(p)
                        return 0
                else:
                        self.validity[index]=1
                        self.names[index]=name
                        self.ip_addresses[index]=ip
                        self.ports[index]=p
                        return 0

	def removeFromPool(self,name):
		flag=False
		for n in self.names:
			if( n == name ):
				flag=True
		
		if( flag == False ):
			return(1)

		self.validity[self.names.index(name)]=0
		return(0)		
