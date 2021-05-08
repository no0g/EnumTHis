#!/bin/env python3
import os

cyan  = "\033[0;96m"
green   = "\033[0;92m"
white   = "\033[0;97m"
red   = "\033[0;91m"
blue  = "\033[0;94m"
yellow  = "\033[0;33m"
magenta = "\033[0;35m"
Color_Off='\033[0m'

def find_files(con):
    con.sendall(b'\nSpecify Dir: ')
    try:
        optDir = con.recv(2048)
        con.sendall(b'\nSpecify Keyword for Files: ')
        optFile = con.recv(2048)
        result = []
        optDir = str(optDir.decode().strip())
        optFile = str(optFile.decode().strip())
        for root, dir, files in os.walk(optDir):
            if optFile in files :
                result.append(os.path.join(root,optFile))
        message = blue+"\nFinding Files . . .\n"
        out = yellow+"\n".join(result)
        con.sendall(str(message+out+"\n").encode())
    except ValueError:
        con.sendall(b"\nPlease send valid input")
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        con.sendall(b"Failed\n")
  

def listDir(con):
    con.sendall(b'\nSpecify Dir: ')
    optDir = con.recv(2048)
    try:
        optDir = str(optDir.decode().strip())
        result = []
        for x in os.listdir(optDir):
            if os.path.isfile(os.path.join(optDir, x)): result.append(white+'f- '+ x)
            elif os.path.isdir(os.path.join(optDir, x)): result.append(blue+'d- '+ x)
            elif os.path.islink(os.path.join(optDir, x)): result.append('l- '+ x)
            else: result.append('--- '+ x)

        listdir = blue+Color_Off+"\n".join(result) 
        listdir = listdir+"\n"
        message = yellow+"Listing Directory "+red+optDir+"\n"
        #con.sendall(message.encode())
        con.sendall(str(message+listdir).encode())
    except ValueError:
        con.sendall(b'Please only send valid input')
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        con.sendall(b'Could Not Retrieve Data')

def filesMenu(con):
    menu = b"\n1. Current Directory\n2. Directory Listing\n3. Find Files in Directory\n"
    con.sendall(menu)
    con.sendall(b"\nSpecify Options: ")
    opt = con.recv(1024)
    try:
        opt = opt.decode()
        opt = int(opt)
        if(opt == 1):
            con.sendall(str(red+os.getcwd()+"\n").encode())
        elif( opt == 2):
            #con.sendall(b'\nListing file ready')
            listDir(con)
        elif(opt == 3):
            find_files(con)
    except ValueError:
        con.sendall(b"\nPlese only send integer value representing each option\n")
    except KeyboardInterrupt:
        sys.exit(0)


