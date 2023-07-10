import sys
import json
import socket
import time
import os
import subprocess
from handleCommunication import HandleCommunication

byt = 1024 * 10


# message Generator
def generate_Message(msg):
    try:
        jsondata = json.dumps(msg)
        return jsondata.encode()
    except Exception as ex:
        print(f"[-] generate message error :{str(ex)}")
        return ""


# send message
def send_Message(clientsocket: socket.socket, command):
    try:
        clientsocket.send(generate_Message(command))
    except Exception as ex:
        print(f"[-]SOMETHING WENT WRONG WHILE SENDING MESSAGE :{str(ex)}")


# received_Message
def receive_Message(clientsocket: socket.socket):
    data = ""
    while True:
        try:
            data = data + clientsocket.recv(byt).decode().rstrip()
            return json.loads(data)
        except socket.error:
            print(f"[-] CONNECTION CLOSED")
            exit()
        except Exception as ex:
            print(f"[-]SOMETHING WENT WRONG WHILE RECEIVING MESSAGE:{str(ex)}")
            exit()


def main():
    if len(sys.argv) != 3:
        print("[+] Usage python ./server.py IP PORT")
        print("[+] Example python ./server.py 192.168.0.151 8000")
        return
    # EXTRACT IP_ADDRESS
    IP_ADDRESS = sys.argv[1]
    PORT = int(sys.argv[2])
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((IP_ADDRESS, PORT))
        while True:
            msg = receive_Message(sock)
            print(msg)
    except Exception as ex:
        print(f"[-] Error :{str(ex)}")
        exit()


if __name__ == "__main__":
    main()
