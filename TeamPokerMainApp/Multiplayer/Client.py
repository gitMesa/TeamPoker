from TeamPokerMainApp.Common.VariableDefinitions import *
from TeamPokerMainApp.Common.MethodDefinitions import *
import socket


class ClientClass:

    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (ip, port)

    def connect_to_server_and_get_position(self):
        try:
            self.client.connect(self.addr)
            handshake_reply = self.client.recv(BUFFERSIZE).decode()
            return handshake_reply
        except Exception as e:
            print(f'connect_to_server_and_get_position -> {e}')

    # Dealer is the first to send a update.
    # When dealer sends update, users will listen to it, and responde with their update.
    # Which then goes back into the Dealer Listening part and cycle repeats.

    def client_communicate_with_server(self, own_data):
        try:
            self.client.sendall(dict_to_string(own_data).encode(FORMAT))
            server_data = self.client.recv(BUFFERSIZE).decode(FORMAT)
            return string_to_dict(server_data)
        except socket.error as e:
            print(f'client_communicate_with_server -> {e}')

