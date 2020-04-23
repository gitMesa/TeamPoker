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
                            # Update the Player-Client fields.
                            self.copy_client_player_fields_to_server_data(client_data_dict, client_number)
                            if client_number == DEALER:
                                # Update the Player-Dealer fields.
                                self.copy_dealer_player_fields_to_server_data(client_data_dict)
                                # Update the Dealer fields.
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

    # Client Updates only certain fields in the PLAYER dictionary, the others (like money available, cards) are edited by the dealer.
    #
    #        self.PLAYER_FIELDS = {"Name": str(""),
    #                           "Icon": str(""),
    #                           "TableSpot": int(0),
    #                           "ConnectionStatus": CONN_STATUS_EMPTY_SEAT,
    #                           "GameStatus": GAME_STATUS_PLAYER_SIT_OUT_TURN,
    #                           "GameAction": ACTION_UNDECIDED,
    #                           "DealerStatus": TABLE_STATUS_is_NORMAL_PLAYER,
    #                           "DealerIcon": str(""),
    #                           "BlindStatus": TABLE_STATUS_is_NORMAL_PLAYER,
    #                           "BlindIcon": str(""),
    #                           "BetAmount": float(0.0),
    #                           "MoneyAvailable": float(0.0),
    #                           "PlayerCards": [NO_CARD, NO_CARD]}

    def copy_client_player_fields_to_server_data(self, client_data, client_number):
        self.server_data_dict["Player"][client_number]["Name"] = client_data["Player"][client_number]["Name"]
        self.server_data_dict["Player"][client_number]["Icon"] = client_data["Player"][client_number]["Icon"]
        self.server_data_dict["Player"][client_number]["TableSpot"] = client_data["Player"][client_number]["TableSpot"]
        self.server_data_dict["Player"][client_number]["ConnectionStatus"] = client_data["Player"][client_number]["ConnectionStatus"]
        self.server_data_dict["Player"][client_number]["GameStatus"] = client_data["Player"][client_number]["GameStatus"]
        self.server_data_dict["Player"][client_number]["GameAction"] = client_data["Player"][client_number]["GameAction"]

    def copy_dealer_player_fields_to_server_data(self, client_data):
        for player in range(MAX_CLIENTS):
            if self.server_data_dict["Player"][player]["GameStatus"] is GAME_STATUS_PLAYER_PLAYING:
                self.server_data_dict["Player"][player]["DealerStatus"] = client_data["Player"][player]["DealerStatus"]
                self.server_data_dict["Player"][player]["DealerIcon"] = client_data["Player"][player]["DealerIcon"]
                self.server_data_dict["Player"][player]["BlindStatus"] = client_data["Player"][player]["BlindStatus"]
                self.server_data_dict["Player"][player]["BetAmount"] = client_data["Player"][player]["BetAmount"]
                self.server_data_dict["Player"][player]["MoneyAvailable"] = client_data["Player"][player]["MoneyAvailable"]
                self.server_data_dict["Player"][player]["PlayerCards"] = client_data["Player"][player]["PlayerCards"]
