#!/bin/env python3
import socket
import sys
from network import *
from files import * 
host = '0.0.0.0'
port = 9001

cyan  = "\033[0;96m"
green   = "\033[0;92m"
white   = "\033[0;97m"
red   = "\033[0;91m"
blue  = "\033[0;94m"
yellow  = "\033[0;33m"
magenta = "\033[0;35m"
Color_Off='\033[0m'

def banner(con):
    banner = magenta + """ 
    8888888888                             88888888888 888    888 d8b          
    888                                        888     888    888 Y8P""" + Color_Off
    banner += yellow + """
    888                                        888     888    888              
    8888888    88888b.  888  888 88888b.d88b.  888     8888888888 888 .d8888b""" + Color_Off
    banner += blue + """
    888        888 "88b 888  888 888 "888 "88b 888     888    888 888 88K      
    888        888  888 888  888 888  888  888 888     888    888 888 "Y8888b.""" + Color_Off
    banner += red + """ 
    888        888  888 Y88b 888 888  888  888 888     888    888 888      X88 
    8888888888 888  888  "Y88888 888  888  888 888     888    888 888  88888P'""" + Color_Off
    con.sendall(banner.encode())


def menu(con):
    banner(con)
    mainMenu = b'\n\nChoose What To Retrieve!\n1. OS Information\n2. Process Information\n3. Information about Mama\n4. Network Information\n5. File and Directory\n'
    con.sendall(mainMenu)
    con.sendall(b'\nSpecify Option: ')
    opt = con.recv(1024)
    if not opt:
        menu()
    else :
        try:
            opt = opt.decode()
            opt = int(opt)
            if(opt == 1):
                con.sendall(b'kerjaan willi')
            elif(opt == 4):
                NetworkMenu(con)
            elif(opt == 5):
                filesMenu(con)
            else :
                con.sendall(b'lol\n')
        except ValueError:
            con.sendall(b'Please only send integer value representing each option\n')
        except KeyboardInterrupt:
            sys.exit(0)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connection from ',addr)
                while True:
                    menu(conn)
        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            sys.exit(0)
        except :
            print('Cant Bind Socket')


if __name__ == "__main__":
    while True:
        main()


