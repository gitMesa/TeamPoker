from TeamPokerMainApp.PokerGame.Multiplayer.NetworkPacket import *
from TeamPokerMainApp.Common.VariableDefinitions import *
from TeamPokerMainApp.Common.MethodDefinitions import *
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
        conn.send(str(client_number).encode(FORMAT))
        while True:
            try:
                # GET Client Data
                client_data = conn.recv(BUFFERSIZE).decode(FORMAT)
                client_data_dict = string_to_dict(client_data)

                # GET Server Data (Thread-Safe)
                while True:
                    if self.mutex.tryLock():
                        # Update server data from client data
                        if client_number == DEALER:
                            # If i'm the dealer, update everything inside.
                            self.server_data_dict["Dealer"] = client_data_dict["Dealer"]
                            self.server_data_dict["PlayersGame"] = client_data_dict["PlayersGame"]
                        else:
                            # If i'm just a player, update only my PlayersInfo
                            self.server_data_dict["PlayersInfo"][client_number] = client_data_dict["PlayersInfo"][client_number]
                        # Send the updated info back to the client:
                        server_data = dict_to_string(self.server_data_dict)
                        # Unlock the server_data_dict for other threads.
                        self.mutex.unlock()
                        break
                print(f'SERVER: Communication update finished for C{client_number}.')
                conn.sendall(server_data.encode(FORMAT))
            except socket.error as e:
                print(f'SERVER: main_communication_loop -> {e}')
                self.conn_player_number -= 1
                conn.close()
                break

