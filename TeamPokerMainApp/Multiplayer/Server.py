from TeamPokerMainApp.Multiplayer.NetworkPacket import *
from TeamPokerMainApp.Common.MethodDefinitions import *
from TeamPokerMainApp.Common.VariableDefinitions import *
from PyQt5.Qt import QMutex
import threading
import socket


class MultiplayerServerClass:

    def __init__(self, ip, port):
        self._network_packet = NetworkPacketClass()
        self.server_data_dict = dict.copy(self._network_packet.get_game_data())
        self.mutex = QMutex()
        self.conn_player_number = 0
        self.conn_players_adresses = [0 for x in range(MAX_CLIENTS)]
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.bind((ip, port))
        except socket.error as e:
            str(e)
        self.s.listen(MAX_CLIENTS)
        print("Server Started... Waiting for a connection")
        thread = threading.Thread(target=self.server_listening_for_new_connections_loop, args=())
        thread.start()

    def server_listening_for_new_connections_loop(self):
        while True:
            conn, addr = self.s.accept()
            self.conn_players_adresses[self.conn_player_number] = addr  # save the connected player info
            print(f'SERVER: New Connection Established. Client (C{self.conn_player_number}) from {self.conn_players_adresses[DEALER]}.')
            thread = threading.Thread(target=self.main_communication_loop, args=(conn, self.conn_player_number))
            thread.start()
            self.conn_player_number += 1
            print(f'SERVER: Active connections: {self.conn_player_number}. ')

    def main_communication_loop(self, conn, client_number):
        # Handshake message
        send_simple_message(conn, client_number)
        connected = True
        while connected:
            try:
                # We send 2 messages between client-server.
                # First we find the size of the dictionary we want to send, and tell the server to receive that size.
                # Second we send the dictionary in string format.
                client_data = receive_message_with_size_confirmation(conn)
                client_data_dict = transform_into_data(client_data)

                # GET Server Data (Thread-Safe)
                while True:
                    if self.mutex.tryLock():
                        # Check if player wants to disconnect!
                        if client_data_dict == MESSAGE_DISCONNECTED:
                            self.server_data_dict["Player"][client_number]["ConnectionStatus"] = CONN_STATUS_DISCONNECTED
                            connected = False
                            conn.close()
                            if client_number == DEALER:
                                # It means that the Client0 (one with dealer logic) disconnected. So shut down the server.
                                self.s.shutdown(socket.SHUT_RDWR)
                                self.s.close()
                                print('SERVER: Client0 Disconnected. Shutting down server.')
                        else:
                            # Update server data from client data
                            self.server_data_dict["Player"][client_number] = client_data_dict["Player"][client_number]
                            if client_number == DEALER:
                                self.server_data_dict["Dealer"] = client_data_dict["Dealer"]
                        # Send the updated info back to the client:
                        server_reply = transform_into_string(self.server_data_dict)
                        # Unlock the server_data_dict for other threads.
                        self.mutex.unlock()
                        break
                if connected:
                    send_message_with_size_confirmation(conn, server_reply)
                print(f'SERVER: Communication update finished for C{client_number}.')
            except socket.error as e:
                print(f'SERVER: main_communication_loop -> {e}')
                send_message_with_size_confirmation(conn, MESSAGE_DISCONNECTED)
                self.conn_player_number -= 1
                conn.close()
                break
