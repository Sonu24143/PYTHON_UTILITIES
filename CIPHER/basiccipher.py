#!/usr/bin/python

from sys import argv
shift=[]
shift_length=0
command=argv[1]
key=argv[2]
symbol_table=[ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z' , 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '!', '@', '#', '^', '&', '*', '-', '_', ':', '.', '?', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symol_table_length=len(symbol_table)

def generateShifter(l):
	seed=24
	shift.append(int(seed))
	for i in range(0,l):
		if len(str(seed)) < 2:
			seed=int(str(seed)+'1')
		a=int(str(seed)[len(str(seed))-2])
		b=int(str(seed)[len(str(seed))-1])
		num1=a*b
		num2=a+b
		seed=int(str(num1)+str(num2))
		shift.append(int(seed))
	global shift_length
	shift_length=len(shift)

def encrypt():
        if validate() == 1:
                print "unable to encrypt as it contains unsupported characters"
                exit(1)
	temp_str=key
	length=len(temp_str)
	result=''
	for i in range(0,length):
                index=symbol_table.index(temp_str[i])
		switched_index=(index+(shift[i%shift_length]%symol_table_length))%symol_table_length
		result+=symbol_table[switched_index]
#                print str(index)+" : "+str(symbol_table[index])
#                print shift[i%shift_length]
#                print str(switched_index)+" : "+str(symbol_table[switched_index])
	print(result)

def decrypt():
	if validate() == 1:
		print "unable to decrypt as it contains unsupported characters"
		exit(1)
        temp_str=key
        length=len(temp_str)
        result=''
        for i in range(0,length):
	        index=symbol_table.index(temp_str[i])
                switched_index=((index-(shift[i%shift_length]%symol_table_length))+symol_table_length)%symol_table_length
                result+=symbol_table[switched_index]
#		print str(index)+" : "+str(symbol_table[index])
#		print shift[i%shift_length]
#		print str(switched_index)+" : "+str(symbol_table[switched_index])
        print(result)

def validate_password():
	temp_str=key
        length=len(temp_str)
	invalid=0
	for i in range(0,length):
		try:
                        index=symbol_table.index(temp_str[i])
		except ValueError:
			print("Unsupported character: "+str(temp_str[i]))
			invalid=1
			continue
	if invalid == 0:
		print("Password valid for encryption")
		return 0
	return 1

def validate():
        temp_str=key
        length=len(temp_str)
        invalid=0
        for i in range(0,length):
                try:
                        index=symbol_table.index(temp_str[i])
                except ValueError:
                        invalid=1
			break
        if invalid == 0:
                return 0
        return 1


def Main():
	generateShifter(10)
	if command == 'encrypt':
		encrypt()
	elif command == 'decrypt':
		decrypt()
	elif command == 'validate':
		validate_password()
	else:
		print("Unknown command")
		exit(1)
	exit(0)


if __name__ == '__main__':
	Main()
