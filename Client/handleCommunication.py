import json
import socket

class HandleCommunication:
    def __init__(self) -> None:
        self.byt=1024*10
        pass
    
    # message Generator
    def generate_Message(self, msg):
        try:
            jsondata = json.dumps(msg)
            return jsondata.encode()
        except Exception as ex:
            print(f"[-] generate message error :{str(ex)}")
            return ""

    # send message
    def send_Message(self, clientsocket: socket.socket, command):
        try:
            clientsocket.send(self.generate_Message(command))
        except Exception as ex:
            print(
                f"[-]SOMETHING WENT WRONG WHILE SENDING MESSAGE :{str(ex)}"
            )


    # received_Message
    def receive_Message(self, clientsocket: socket.socket):
        data = ""
        while True:
            try:
                data = data + clientsocket.recv(self.byt).decode().rstrip()
                return json.loads(data)
            except Exception as ex:
                print(
                    f"[-]SOMETHING WENT WRONG WHILE RECEIVING MESSAGE:{str(ex)}"
                )
                return data