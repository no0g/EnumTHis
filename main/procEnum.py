#!/bin/env python3

import psutil
import os
import platform

cyan  = "\033[0;96m"
green   = "\033[0;92m"
white   = "\033[0;97m"
red   = "\033[0;91m"
blue  = "\033[0;94m"
yellow  = "\033[0;33m"
magenta = "\033[0;35m"
Color_Off='\033[0m'

def listProc():
    if platform.system() == "Windows":
    	output = os.popen('wmic process get description, processid').read()
    else:
    	p = os.popen('ps -aux')
    	output = p.read()
    return output
    
def procInfo(con):
    con.sendall(b'\nSpecify PID: ')
    pid = con.recv(2048)
    try:
        pid = pid.decode()
        pid = int(pid)
        pName = psutil.Process(int(pid)).name()
        pStatus = psutil.Process(int(pid)).status()
        pUsername = psutil.Process(int(pid)).username()
        pExe = psutil.Process(int(pid)).exe()
        pCwd = psutil.Process(int(pid)).cwd()
        
        fullInfo = "Here are the information for PID "+yellow+str(pid)+Color_Off+"\nProcess Name: "+green+str(pName)+Color_Off+"\nProcess Status: "+blue+str(pStatus)+Color_Off+"\n"+magenta+str(pUsername)+Color_Off+" owns the process"+"\nProcess executable absolute path: "+cyan+str(pExe)+Color_Off+"\nProcess current working directory: "+red+str(pCwd)+Color_Off+"\n"
        
        con.sendall(str(fullInfo).encode())
    except ValueError:
        con.sendall(b'Please only send valid input')
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        con.sendall(b'Could Not Retrieve Data')

def procPC(con):
    con.sendall(b'\nSpecify PID: ')
    pid = con.recv(2048)
    try:
        pid = pid.decode()
        pid = int(pid)
        pParent = psutil.Process(int(pid)).parents()
        parentStr = ' '.join([str(elem) for elem in pParent])
        pChild = psutil.Process(int(pid)).children(recursive=True)
        childStr = ' '.join([str(elem) for elem in pChild])
        pcInfo = "Here are the parent and children process for PID "+green+str(pid)+Color_Off+"\nParent Process: "+yellow+str(parentStr)+Color_Off+"\nChild Process: "+blue+str(childStr)+Color_Off+"\n"
        
        con.sendall(str(pcInfo).encode())
        
    except ValueError:
        con.sendall(b'Please only send valid input')
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        con.sendall(b'Could Not Retrieve Data')

def procMenu(con):
    menu = b"\n1. List available processes\n2. List Process Information\n3. List process parent and child information\n"
    con.sendall(menu)
    con.sendall(b"\nSpecify Options: ")
    opt = con.recv(1024)
    try:
        opt = opt.decode()
        opt = int(opt)
        if(opt == 1):
            result = listProc()
            con.sendall(str(result).encode())
        elif(opt == 2):
            procInfo(con)
        elif(opt == 3):
            procPC(con)
    except ValueError:
        con.sendall(b"\nPlese only send integer value representing each option\n")
    except KeyboardInterrupt:
        sys.exit(0)




if __name__ == "__main__":
    a = procPC()
    print(a)
    