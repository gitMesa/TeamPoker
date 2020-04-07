from TeamPokerMainApp.Common.VariableDefinitions import *
import socket
import json


class ClientClass:

    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (ip, port)

    def connect_to_server_and_get_player_position(self):
        return self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            handshake_reply = self.client.recv(BUFFERSIZE).decode()
            print(f'Connected to the server, my player index is: {handshake_reply}')
            return handshake_reply
        except Exception as e:
            print(e)

    def send_and_receive_update(self, data):
        try:
            self.client.sendall(self.dict_to_string(data).encode())
            recvd = self.client.recv(BUFFERSIZE).decode()
            print(f'received back from server {type(recvd)}')
            return self.string_to_dict(recvd)
        except socket.error as e:
            print(e)

    def send_dealer_update_to_server(self, data):
        try:
            self.client.sendall(self.dict_to_string(data).encode())
        except socket.error as e:
            print(e)

    def dict_to_string(self, dict):
        newDict = json.dumps(dict)
        type(newDict)
        return newDict

    def string_to_dict(self, string):
        newDict = json.loads(string)
        type(newDict)
        return newDict
