#!/bin/env python3

import netifaces
import pickle
import json
from socket import gethostname

cyan  = "\033[0;96m"
green   = "\033[0;92m"
white   = "\033[0;97m"
red   = "\033[0;91m"
blue  = "\033[0;94m"
yellow  = "\033[0;33m"
magenta = "\033[0;35m"
Color_Off='\033[0m'

def getInterfaces():
    interfaces = netifaces.interfaces()
    interface_str = ", ".join(interfaces)
    return yellow+interface_str+Color_Off

def getIPaddress(con):
    
    interfaces = getInterfaces()
    interfaces = interfaces+"\n\n"
    con.sendall(str(interfaces+"\nSpecify Interface: ").encode())
    #con.sendall(b"\nSpecify Interface: ")
    optInt = con.recv(1024)
    try:
        optInt = str(optInt.decode().strip())
        address = netifaces.ifaddresses(optInt)
        address = address[netifaces.AF_INET]
        address = address[0]
        address = blue+"ip: "+green+address["addr"]+blue+", netmask: "+green+address["addr"]+Color_Off+"\n\n"
        con.sendall(address.encode())
    except ValueError:
        con.sendall(b'Please only send valid input')
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        con.sendall(b'Could Not Retrieve Data')

def getMacAddress(con):
    interfaces = getInterfaces()
    interfaces = interfaces+"\n\n"
    con.sendall(str(interfaces+"\nSpecify Interface: ").encode())
    #con.sendall(b"\nSpecify Interface: ")
    optInt = con.recv(1024)
    try:
        optInt = str(optInt.decode().strip())
        address = netifaces.ifaddresses(optInt)
        address = address[netifaces.AF_LINK]
        address = address[0]
        address = blue+"MAC Address: "+green+address["addr"]+Color_Off+"\n\n"
        con.sendall(address.encode())
    except ValueError:
        con.sendall(b'Please only send valid input')
    except KeyboardInterrupt:
        sys.exit(0)
    except :
        con.sendall(b'Could Not Retrieve Data')

def networkMenu(con):
    menu = b'1. Get All Network Interfaces\n2. Get IP Address\n3. Get Mac Address\n4. Get Hostname'
    con.sendall(menu)
    con.sendall(b"\nSpecify Options: ")
    opt = con.recv(1024)
    try:
        opt = opt.decode()
        opt = int(opt)
        if( opt == 1):
            #con.sendall(b'Listing Out Network Interfaces:\n')
            interfaces = getInterfaces()
            interfaces = interfaces+"\n\n"
            con.sendall(str("Listing Out Network Interfaces:\n"+interfaces).encode())
        elif (opt == 2):
            #con.sendall(b'Retrieving IP address\n')
            getIPaddress(con)
        elif (opt == 3): 
            #con.sendall(b'Get Mac Address from Interface\n')
            getMacAddress(con)
        elif (opt == 4):
            #con.sendall(b'Get Hostname\n')
            hostname = gethostname()
            hostname = str("\nHostname:"+red+hostname+Color_Off+"\n").encode()
            con.sendall(hostname)
    except ValueError:
        con.sendall(b'Please only send integer value representing each option\n')
    except KeyboardInterrupt:
        sys.exit(0)

