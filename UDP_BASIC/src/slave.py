#!/usr/bin/python
#SLAVE
import socket
from sys import argv
import thread
import os

os.system('clear')

MESSAGE_SIZE=2048
SEND_SOCKET = socket.socket( socket.AF_INET , socket.SOCK_DGRAM )
LISTEN_SOCKET = socket.socket( socket.AF_INET , socket.SOCK_DGRAM )
id_name=""
my_name=""

def initialize(server_address,port):
        global id_name
	global my_name
        id_name=raw_input("Enter your name: ")
	my_name=id_name
	file=open(my_name,"w")
	file.write("######### MESSENGER #########\n")
	file.close()
        connection_request="CONNECTION_REQUEST:"+str(port)+":"+id_name
        SEND_SOCKET.sendto(connection_request,server_address)
        return 0

def destroyConn(server_address):
        disconnect_request="DISCONNNECT_REQUEST:"+id_name
        SEND_SOCKET.sendto(disconnect_request,server_address)
        print("Disconnected")

def process(msg):
	print msg
        if ( msg == "RESPONSE:SUCCESS"):
                print("Connection successful")
        else:
		file=open(my_name,"a")
		file.write(msg+"\n")
		file.close()

def draw_file():
	os.system("clear")
	file=open(my_name,"r")
	for line in file:
		print line
	file.close()

def listener( s , a ):
        s.bind(a)
        while True:
                msg , addr = s.recvfrom( MESSAGE_SIZE )
                process(msg)
		draw_file()

def Main():
        if len(argv) != 5:
                print("Please use the right format ./slave.py server_ip server_port local_ip local_port")
                exit(1)
        SERVER_IP=argv[1]
        SERVER_PORT=int(argv[2])
        LOCAL_IP=argv[3]
        LOCAL_PORT=int(argv[4])
        SERVER_ADDRESS = ( SERVER_IP , SERVER_PORT )
        LOCAL_ADDRESS = ( LOCAL_IP , LOCAL_PORT )
        try:
                thread.start_new_thread( listener , (LISTEN_SOCKET,LOCAL_ADDRESS,) )
        except Exception as errtxt:
                print errtxt
        initialize(SERVER_ADDRESS,LOCAL_PORT)
        while True:
		global id_name
                message=raw_input()
		if ( message.strip(" ").rstrip(" ") == "STATE" ):
			if( id_name == my_name ):
				print("Not connected to any users")
				continue
			print("Connected to "+id_name)
			continue
		if ( len(message.split(" ")) == 3 and message.split(" ")[0].strip(" ") == "connect" and message.split(" ")[1].strip(" ") == "to" ):
			id_name=str(message.split(" ")[2])
			print("Connected to : "+id_name)
			continue
                if ( len(message.split(" ")) == 1 and message.strip(" ").rstrip(" ") == "disconnect" ):
			temp=id_name
                        id_name=my_name
			print("Disconnected from "+temp+" ...")
                        continue
		if ( message.strip(" ").rstrip(" ") == "GETUSERS" and id_name != my_name ):
			print("You are connected to USER: "+id_name+", please disconnect \nand the list connected users")
			continue

                if ( message == "bye" or message == "Bye" or message == "BYE" ):
                        destroyConn(SERVER_ADDRESS)
			with( open(my_name."w" ):
				pass
                        break
		if ( my_name != id_name ):
			file=open(my_name,"a")
			file.write(my_name+": "+message+"\n")
			file.close()
                SEND_SOCKET.sendto("MESSAGE_TEXT:"+id_name+":"+my_name+":"+message,SERVER_ADDRESS)
        exit(0)

if __name__ == "__main__":
        Main()
