import socket as soc
import threading as th

server=soc.socket(soc.AF_INET,soc.SOCK_STREAM)
server.bind(("0.0.0.0",12345))
server.listen()
clients=[]
adresler=[]


def girdi():
    while True:
        try:
            a=input("")
            if(a=="help"):
                print("kapat: serverı kapatmak için")
                print("ban: birisini sunucudan atmak için")
            elif(a=="kapat"):
                closer()
                server.close()
                print("kapandı bay bay")
                break
            elif(a=="ban"):
                ip=input("ip gir >")
                clients[adresler.index(ip)].send("öldün".encode())
                clients[adresler.index(ip)].close()
                clients.remove(clients[adresler.index(ip)])
        except KeyboardInterrupt:
            print("yavaş bas ctrl+c'ye")

def asd():
    while True:
        try:
            conn,addr=server.accept()
            nickname=conn.recv(1024).decode()
            print(f"{addr}:{nickname} ismi ile bağlandı bağlandı")
            sender("giriş yaptı",nickname)
            clients.append(conn)
            adresler.append(addr[0])
            th.Thread(target=naber,args=(conn,nickname)).start()
        except:
            server.close()
            print("server kapandı")
            break

def sender(message,nickname):
    for i in clients:
        if(message!="" or message is not None):
            i.send(f"{nickname} : ".encode() + message.encode())
        else:
            pass

def closer():
    for i in clients:
        try:
            i.send("kapandı beyler".encode())
        except:
            pass

def naber(client,nickname):
    while True:
        try:
            msg=client.recv(1024).decode()
            if(msg!="ben kaçar"):
                sender(msg,nickname)
            else:
                clients.remove(client)
                client.close()
                print(f"{nickname}: çıktı")
                sender("çıkış yaptı",nickname)
                break
        except:
            pass

th.Thread(target=asd,daemon=True).start()
th.Thread(target=girdi).start()
th.Thread(target=sender,args=("",""),daemon=True).start()
