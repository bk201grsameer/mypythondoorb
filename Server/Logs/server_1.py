# Get-Content -Path .\Server\Logs.txt -Wait
import socket
import threading
import json
import os
import sys


def print_thread_count(f):
    thread_count = threading.active_count()
    f.write(f"[+] Number of active threads: {thread_count-1}\n")


def clear_line(dir):
    sys.stdout.write("\033[2K")  # Clear current line
    if dir == 0:
        sys.stdout.write("\033[1G")  # Move cursor to the beginning of the line
    else:
        sys.stdout.write("\033[999C")  # Move cursor to the end of the line
    sys.stdout.flush()


def move_cursor(dx, dy):
    if dx > 0:
        sys.stdout.write("\033[%dC" % dx)  # Move cursor right by dx columns
    elif dx < 0:
        sys.stdout.write("\033[%dD" % (-dx))  # Move cursor left by dx columns

    if dy > 0:
        sys.stdout.write("\033[%dB" % dy)  # Move cursor down by dy rows
    elif dy < 0:
        sys.stdout.write("\033[%dA" % (-dy))  # Move cursor up by dy rows

    sys.stdout.flush()


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
        print(f"[+] Server listening on {self.serverIP}:{self.serverPORT}")
        with open("Logs.txt", "a") as f:
            while True:
                try:
                    f.write("[+] WAITING FOR INCOMING REQUESTS\n")
                    f.flush()
                    client, address = self.server.accept()
                    f.write(f"[+] CLIENT CONNECTED FROM {address[0]}:{address[1]}\n")
                    f.flush()
                    print_thread_count(f)
                    f.flush()
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
