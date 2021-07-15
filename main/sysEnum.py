#!/bin/env python3
import platform
import psutil

cyan  = "\033[0;96m"
green   = "\033[0;92m"
white   = "\033[0;97m"
red   = "\033[0;91m"
blue  = "\033[0;94m"
yellow  = "\033[0;33m"
magenta = "\033[0;35m"
Color_Off='\033[0m'

def processor():
    name = platform.processor()
    phyCore = psutil.cpu_count(logical=False)
    totCore = psutil.cpu_count(logical=True)
    
    procInfo = "Processor's name is "+red+name+Color_Off+"\nThe user have "+red+str(phyCore)+" physical core(s) and "+red+str(totCore)+" total core(s)\n"+Color_Off
    return procInfo

def hardwareInfo():
    desktopName = platform.node()
    return red+desktopName+Color_Off

def architecture():
    architecture_details = platform.architecture()
    delimiter = ','
    detail = delimiter.join(architecture_details)
    return green+detail+Color_Off

def sysMenu(con):
    menu = b"\n1. Processor Information\n2. Hardware Name\n3. System Architecture\n"
    con.sendall(menu)
    con.sendall(b"\nSpecify Options: ")
    opt = con.recv(1024)
    try:
        opt = opt.decode()
        opt = int(opt)
        if(opt == 1):
            name = processor()
            con.sendall(str(name).encode())
        elif(opt == 2):
            name = hardwareInfo()
            con.sendall(str("User's computer network name is "+name).encode())
        elif(opt == 3):
            result = architecture()
            con.sendall(str("User's desktop system architecture is "+result).encode())
    except ValueError:
        con.sendall(b"\nPlese only send integer value representing each option\n")
    except KeyboardInterrupt:
        sys.exit(0)
        
if __name__ == "__main__":
    a = processor()
    b = hardwareInfo()
    c = architecture()
    print(a)
    print(b)
    print(c)