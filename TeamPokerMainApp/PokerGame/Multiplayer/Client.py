from TeamPokerMainApp.Common.VariableDefinitions import *
import socket
import json


class ClientClass:

    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (ip, port)
        self.data = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            rtrn = self.client.recv(BUFFERSIZE).decode(encoding='utf-8')
            print(rtrn)
            return rtrn
        except Exception as e:
            print(e)

    def send_and_receive_update(self, data):
        try:
            self.client.send(json.dumps(data))
            return self.client.recv(BUFFERSIZE).decode(encoding='utf-8')
        except socket.error as e:
            print(e)
