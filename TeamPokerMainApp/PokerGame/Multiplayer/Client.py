from TeamPokerMainApp.Common.VariableDefinitions import *
import socket


class ClientClass:

    def __init__(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (ip, port)

    def connect_to_server_and_get_player_position(self):
        try:
            self.client.connect(self.addr)
            handshake_reply = self.client.recv(BUFFERSIZE).decode()
            print(f'CLIENT: Server Connection Established. My player index is: {handshake_reply}')
            return handshake_reply
        except Exception as e:
            print(f'connect_to_server_and_get_player_position -> {e}')

    def send_client_data_and_receive_dealer_data(self, data):
        try:
            self.client.sendall(str(data).encode())
            recvd = self.client.recv(BUFFERSIZE).decode()
            return str(recvd)
        except socket.error as e:
            print(f'send_client_data_and_receive_dealer_data -> {e}')

    def send_dealer_update_to_server(self, data):
        try:
            # print(f'CLIENT-SIDE: {type(data)} -> {data}')
            self.client.sendall(self.dict_to_string(data).encode())
        except socket.error as e:
            print(f'send_dealer_update_to_server -> {e}')

    def dict_to_string(self, dict):
        return str(dict)

    def string_to_dict(self, string):
        return eval(string)
