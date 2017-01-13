#!/usr/bin/python
import socket
from sys import argv
import thread
import os

os.system('clear')

MESSAGE_SIZE=2048

def process(msg):
	print("GUEST : "+msg)

def listener( s , a ):
	s.bind(a)
	while True:
		msg , addr = s.recvfrom( MESSAGE_SIZE )
		print addr[0]
		process(msg)	

def Main():
	if len(argv) != 5:
		print("Please use the right format ./bot.py listen_port sen_ip send_port")
		exit(1)
	HOST_IP=argv[1]
	IN_PORT=int(argv[2])
	GUEST_IP=argv[3]
	OUT_PORT=int(argv[4])	
	UDP_CLIENT_SENDER = socket.socket( socket.AF_INET , socket.SOCK_DGRAM )
	UDP_SERVER_LISTEN = socket.socket( socket.AF_INET , socket.SOCK_DGRAM )
	GUEST_ADDRESS = ( GUEST_IP , OUT_PORT )
	LOCAL_ADDRESS = ( HOST_IP , IN_PORT )
	try:
		thread.start_new_thread( listener , (UDP_SERVER_LISTEN,LOCAL_ADDRESS,) )
	except Exception as errtxt:
		print errtxt
	message=""
	print("########## CHATBOT ##########")
	while True:
		message=raw_input()
		UDP_CLIENT_SENDER.sendto(message,GUEST_ADDRESS)
		if ( message == "bye" or message == "Bye" or message == "BYE" ):
			break
	exit(0)

if __name__ == "__main__":
	Main()
