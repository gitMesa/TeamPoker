from TeamPokerMainApp.Common.MethodDefinitions import *
import socket


class ClientCommunicationClass:

    def __init__(self, ip_port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = ip_port

    def client_connect_to_server_and_get_position(self):
        try:  # Handshake message
            self.client.connect(self.addr)
            client_index = receive_simple_message(self.client)
            return client_index
        except Exception as e:
            print(f'client_connect_to_server_and_get_position -> {e}')

    def client_send_message_to_server_return_reply(self, message):
        try:
            # Send the message with confirmation to the server
            send_message_with_size_confirmation(self.client, message)
            # Receive the reply with confirmation from the server
            reply = receive_message_with_size_confirmation(self.client)
            return transform_into_data(reply)

        except socket.error as e:
            print(f'client_send_message_to_server_return_reply -> {e}')

