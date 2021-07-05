#!/bin/env python3

import psutil
import platform

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


if __name__ == "__main__":
    print(getCPUUsage())
    print(getRAMUsage())
    print(getDiskUsage())