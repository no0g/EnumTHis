#!/bin/env python3

import socket

def netcat(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, int(port)))
    s.shutdown(socket.SHUT_WR)
    while True:
        data = s.recv(4096)
        if not data:
            break
        print(repr(data))
    content = input()
    s.sendall(content.encode())


host = input("Enter IP: ")
port = input("Enter Port: ")

try:
    while True:
        netcat(host.strip(),port.strip())
except KeyboardInterrupt:
    sys.exit(0)
