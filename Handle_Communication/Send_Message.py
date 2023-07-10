from abc import ABC, abstractmethod
import socket


# interface to be implemented
class MessageSender_Server(ABC):
    @abstractmethod
    def send_Message(self, clientsocket: socket.socket, command, current_clientip):
        pass


class MessageSender_Client(ABC):
    @abstractmethod
    def send_Message(self, clientsocket: socket.socket, command):
        pass
