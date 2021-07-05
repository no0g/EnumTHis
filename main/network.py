#!/bin/env python3
import re, uuid
import psutil

cyan  = "\033[0;96m"
green   = "\033[0;92m"
white   = "\033[0;97m"
red   = "\033[0;91m"
blue  = "\033[0;94m"
yellow  = "\033[0;33m"
magenta = "\033[0;35m"
Color_Off='\033[0m'

def getNetInterface():
    result = psutil.net_if_addrs()
    netInterface = ""
    result = list(result.keys())
    for i in result:
        netInterface+= blue
        netInterface+= i
        netInterface+= ", "
        netInterface+=Color_Off
    return netInterface

def getIPAddress():
    result = psutil.net_if_addrs()
    interface = list(result.keys())
    ip = []
    for i in interface:
        ip.append(green+result[i][0].address)
    
    all = ""
    for i,j in zip(interface,ip):
        all+= magenta
        all += i+ " " + j + "\n"
        all+=Color_Off
    return all
        

def getMacAddress():
    mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    return cyan+mac+Color_Off

def NetworkMenu(con):
    menu = b"\n1. Get Network Interface\n2. Get IP address\n3. Get Mac Address\n"
    con.sendall(menu)
    con.sendall(b"\nSpecify Options: ")
    opt = con.recv(1024)
    try:
        opt = opt.decode()
        opt = int(opt)
        if(opt == 1):
            con.sendall(str(getNetInterface()).encode())
        elif( opt == 2):
            #con.sendall(b'\nListing file ready')
            con.sendall(str(getIPAddress()).encode())
        elif(opt == 3):
            con.sendall(str(getMacAddress()).encode())
    except ValueError:
        con.sendall(b"\nPlese only send integer value representing each option\n")
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    a = getNetInterface()
    b = getIPAddress()
    print(a)
    print(b)
    mac = getMacAddress()
    print(mac)