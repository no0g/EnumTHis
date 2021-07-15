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
    
def kill(con):
    con.sendall(b'\nSpecify PID: ')
    pid = con.recv(2048)
    try:
        pid = pid.decode()
        pid = int(pid)
        p = psutil.Process(pid)
        p.terminate()
        con.sendall(b'\nProcess Terminated!')
    except ValueError:
        con.sendall(b'Please only send valid input')
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        con.sendall(b'Could Not Retrieve Data')

def killProcess(con):
    menu = b"\n1. List available processes\n2. Kill Process\n"
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
            kill(con)
    except ValueError:
        con.sendall(b"\nPlese only send integer value representing each option\n")
    except KeyboardInterrupt:
        sys.exit(0)
