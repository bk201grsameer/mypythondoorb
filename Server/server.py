import subprocess
import socket
import threading
import json
import os
import sys
from Logs.LogsHandler import log_Handler

# logs
logterminal = log_Handler()


def print_thread_count():
    thread_count = threading.active_count()
    logterminal.write(f"[+] Number of active threads: {thread_count-1}")


class Server:
    def __init__(self, IP, PORT) -> None:
        # INITIALIZE THE SOCKETS
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((IP, PORT))
        self.server.listen()
        self.serverIP = IP
        self.serverPORT = PORT
        # LIST OF CLIENTS
        self.ip_to_socket_map = {}
        self.control_Thread = None
        self.current_Client = None
        self.byt = 1024 * 10

    def handle_Clients(self):
        # LOGIC TO HANDLE CLIENTS
        if self.current_Client == None:
            return
        while True and self.current_Client != None:
            try:
                print(f"Shell~{self.current_Client}:> ", end="")
                command = input()
                print(command)
            except Exception as ex:
                pass

    def start(self):
        # LOGIC FOR THE SERVER
        logterminal.write(f"[+] Server listening on {self.serverIP}:{self.serverPORT}")
        while True:
            try:
                logterminal.write(f"[+] WAITING FOR INCOMING REQUESTS")
                client, address = self.server.accept()
                logterminal.write(f"[+] CLIENT CONNECTED FROM {address[0]}:{address[1]}")
                print_thread_count()
                # append the client to the list of clients only once from the same ip
                if self.ip_to_socket_map.get(address[0]) == None:
                    self.ip_to_socket_map[address[0]] = client

                if self.current_Client == None and self.control_Thread == None:
                    # logic to control the clients
                    print(f"[+] Starting a New Thread to control the clients")
                    self.current_Client = address[0]
                    thread = threading.Thread(target=self.handle_Clients)
                    thread.start()
                else:
                    # logic to handle another client joined
                    pass

            except Exception as ex:
                print(f"[-] SOMETHING WENT WRONG IN START _SERVER {str(ex)}")


def main():
    if len(sys.argv) != 3:
        print("[+] Usage python ./server.py IP PORT")
        print("[+] Example python ./server.py 192.168.0.151 8000")
        return
    # EXTRACT IP_ADDRESS
    IP_ADDRESS = sys.argv[1]
    PORT = int(sys.argv[2])
    server = Server(IP_ADDRESS, PORT)
    server.start()


if __name__ == "__main__":
    main()
