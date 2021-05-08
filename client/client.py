#!/bin/env python3

from pwn import *

target = input("Enter your target IP: ")
r = remote(target.strip(),9001)
try:
    while True:
        data = r.recv(4092).decode()
        print(data)
        opt = input()
        opt = opt.encode()
        r.sendline(opt)
except KeyboardInterrupt:
    r.close()
    print("Connection Aborted")
