#!/bin/env python3

import platform 

cyan  = "\033[0;96m"
green   = "\033[0;92m"
white   = "\033[0;97m"
red   = "\033[0;91m"
blue  = "\033[0;94m"
yellow  = "\033[0;33m"
magenta = "\033[0;35m"
Color_Off='\033[0m'

def osName():
    name = platform.system()
    return yellow+name+Color_Off

def osRelease():
    release = platform.release()
    return cyan+release+Color_Off

def osVersion():
    version = platform.version()
    return red+version+Color_Off
    
def osType():
    type = platform.platform()
    return green+type+Color_Off

def machineType():
    machine = platform.machine()
    return magenta+machine+Color_Off
    
def osMenu(con):
    menu = b"\n1. Operating System Name\n2. Operating System Release\n3. Operating System Information\n4. Platform Type\n5. Machine Type\n"
    con.sendall(menu)
    con.sendall(b"\nSpecify Options: ")
    opt = con.recv(1024)
    try:
        opt = opt.decode()
        opt = int(opt)
        if(opt == 1):
            name = osName()
            con.sendall(str("User's operating system name is "+name).encode())
        elif(opt == 2):
            release = osRelease()
            con.sendall(str("User's operating system release is "+release).encode())
        elif(opt == 3):
            version = osVersion()
            con.sendall(str("User's operating system version is "+version).encode())
        elif(opt == 4):
            type = osType()
            con.sendall(str("User's platform type is "+type).encode())
        elif(opt == 5):
            machine = machineType()
            con.sendall(str("User's machine type is "+machine).encode())
    except ValueError:
        con.sendall(b"\nPlese only send integer value representing each option\n")
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == "__main__":
    a = osName()
    b = osRelease()
    c = osVersion()
    d = machineType()
    e = osType()
    print(e)
    print(a)
    print(b)
    print(c)
    print(d)