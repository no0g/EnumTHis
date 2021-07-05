#!/bin/env python3
import socket
import sys
import psutil
import re, uuid
import platform
import os


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

# get net info

def getNetInterface():
    result = psutil.net_if_addrs()
    netInterface = ""
    result = list(result.keys())
    for i in result:
        netInterface+= blue
        netInterface+= i
        netInterface+= ", "
        netInterface+=Color_Off
    return netInterface

def getIPAddress():
    result = psutil.net_if_addrs()
    interface = list(result.keys())
    ip = []
    for i in interface:
        if os.name == 'nt':
            ip.append(green+result[i][1].address)
        else:
            ip.append(green+result[i][0].address)

    
    all = ""
    for i,j in zip(interface,ip):
        all+= magenta
        all += i+ " " + j + "\n"
        all+=Color_Off
    return all
        

def getMacAddress():
    mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    return cyan+mac+Color_Off

def NetworkMenu(con):
    menu = b"\n1. Get Network Interface\n2. Get IP address\n3. Get Mac Address\n"
    con.sendall(menu)
    con.sendall(b"\nSpecify Options: ")
    opt = con.recv(1024)
    try:
        opt = opt.decode()
        opt = int(opt)
        if(opt == 1):
            con.sendall(str(getNetInterface()).encode())
        elif( opt == 2):
            #con.sendall(b'\nListing file ready')
            con.sendall(str(getIPAddress()).encode())
        elif(opt == 3):
            con.sendall(str(getMacAddress()).encode())
    except ValueError:
        con.sendall(b"\nPlese only send integer value representing each option\n")
    except KeyboardInterrupt:
        sys.exit(0)


# get file info
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




# get hardware usage
def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def getCPUUsage():
    usage = green+"Here is the usage of each core:\n"
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        usage += magenta
        usage += "Core {}: {}%\n".format(i,percentage)
    return usage+Color_Off


def getRAMUsage():
    usage = green+"Here is the Memory Usage:\n"
    # get the memory details
    svmem = psutil.virtual_memory()
    usage += magenta
    usage += f"Total: {get_size(svmem.total)}\n"
    usage += f"Available: {get_size(svmem.available)}\n"
    usage += f"Used: {get_size(svmem.used)}\n"
    usage += f"Percentage: {svmem.percent}%\n"
    return usage+Color_Off

def getDiskUsage():
    partitions = psutil.disk_partitions()
    usage = green+"Here is the Disk usage:\n"
    for partition in partitions:
        usage+= red
        usage += f"  Device: {partition.device} \n"
        usage += f"  Mountpoint: {partition.mountpoint}\n"
        usage += f"  File system type: {partition.fstype}\n"
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        usage+= magenta
        usage += f"  Total Size: {get_size(partition_usage.total)}\n"
        usage += f"  Used: {get_size(partition_usage.used)}\n"
        usage += f"  Free: {get_size(partition_usage.free)}\n"
        usage += f"  Percentage: {partition_usage.percent}%\n"
    return usage+ Color_Off

def UsageMenu(con):
    menu = b"\n1. Get CPU Usage\n2. Get Memory Usage\n3. Get Disk Usage\n"
    con.sendall(menu)
    con.sendall(b"\nSpecify Options: ")
    opt = con.recv(1024)
    try:
        opt = opt.decode()
        opt = int(opt)
        if(opt == 1):
            con.sendall(str(getCPUUsage()).encode())
        elif( opt == 2):
            #con.sendall(b'\nListing file ready')
            con.sendall(str(getRAMUsage()).encode())
        elif(opt == 3):
            con.sendall(str(getDiskUsage()).encode())
    except ValueError:
        con.sendall(b"\nPlese only send integer value representing each option\n")
    except KeyboardInterrupt:
        sys.exit(0)


# main
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
    mainMenu = b'\n\nChoose What To Retrieve!\n1. OS Information\n2. Process Information\n3. Information about Mama\n4. Network Information\n5. File and Directory\n6. Hardware Usage\n'
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
            elif(opt == 6):
                UsageMenu(con)
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


