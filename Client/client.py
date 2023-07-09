import sys
import json
import socket
import time
import os
import subprocess


def main():
    if len(sys.argv) != 3:
        print("[+] Usage python ./server.py IP PORT")
        print("[+] Example python ./server.py 192.168.0.151 8000")
        return
    # EXTRACT IP_ADDRESS
    IP_ADDRESS = sys.argv[1]
    PORT = int(sys.argv[2])
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP_ADDRESS, PORT))
    while True:
        # msg = sock.recv(1024 * 10)
        print(input())


if __name__ == "__main__":
    main()
