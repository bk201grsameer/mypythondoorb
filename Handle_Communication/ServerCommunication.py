import socket
from Handle_Communication.Communication import HandleCommunication
from Handle_Communication.Send_Message import *

class Server_Communication(HandleCommunication, MessageSender_Server):
    def __init__(self, logterminal, ip_to_socket_map) -> None:
        super().__init__()
        self.logterminal = logterminal
        self.ip_to_socket_map = ip_to_socket_map
        pass
    # send message
    def send_Message(self, clientsocket: socket.socket, command, current_clientip):
        try:
            clientsocket.send(self.generate_Message(command))
        except Exception as ex:
            self.logterminal.write(
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
                self.logterminal.write(f"[+] NO ACTIVE SESSIONS")
