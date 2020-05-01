from TeamPokerMainApp.GameLogic.CardDeck import CardDeckClass
from TeamPokerMainApp.GameLogic.Dealer import DealerClass
from TeamPokerMainApp.Multiplayer.NetworkPacket import *
from TeamPokerMainApp.Common.MethodDefinitions import *
from PyQt5.Qt import QMutex
import threading
import socket


class MultiplayerServerClass(NetworkPacketClass, CardDeckClass):

    def __init__(self, ip_port, game_rules):
        self.server_data = dict.copy(self.get_network_packet_definition())
        self.setup_game_rules_to_server_data(game_rules)
        self._dealer = DealerClass(data=self.server_data)
        self.mutex = QMutex()
        self.conn_player_number = 0
        self.conn_players_addresses = [0 for x in range(MAX_CLIENTS)]
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.bind(ip_port)
        except socket.error as e:
            str(e)
        self.s.listen(MAX_CLIENTS)
        print("Server Started... Waiting for a connection")
        thread = threading.Thread(target=self.server_listening_for_new_connections_loop, args=())
        thread.start()

    def server_listening_for_new_connections_loop(self):
        while True:
            conn, addr = self.s.accept()
            self.conn_players_addresses[self.conn_player_number] = addr  # save the connected player info
            print(f'SERVER: New Connection Established. Client (C{self.conn_player_number}) from {self.conn_players_addresses[CLIENT_SRV]}.')
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
                client_data = transform_into_data(client_data)

                while True:
                    # Try to access Server Data (Thread-Safe)
                    if self.mutex.tryLock():

                        # Are we still connected to this player?
                        if client_data:
                            self.server_data[PS][client_number][PS_ConnectionStatus] = CONN_STATUS_CONNECTED
                        else:
                            self.server_data[PS][client_number][PS_ConnectionStatus] = CONN_STATUS_DISCONNECTED

                        # Copy the clients data onto the server data.
                        self.server_data[PC][client_number] = client_data[PC][client_number]

                        if client_number == CLIENT_SRV:
                            # The server should theoretically loop through communication with all clients
                            # So if we do the dealer logic only on player0 (DEALER) then we should theoretically
                            # do the dealer logic only once per update to all other clients.

                            self._dealer.dealer_evaluate_next_step()

                        # Send the updated info back to the client:
                        server_reply = transform_into_string(self.server_data)

                        # Unlock the server_data_dict for other threads.
                        self.mutex.unlock()
                        break
                if connected:
                    send_message_with_size_confirmation(conn, server_reply)
                print(f'SERVER: Communication done for C{client_number}.')

            except socket.error as e:
                print(f'SERVER: main_communication_loop -> {e}')
                send_message_with_size_confirmation(conn, MESSAGE_DISCONNECTED)
                self.conn_player_number -= 1
                conn.close()
                break

    def setup_game_rules_to_server_data(self, rules):
        # 0 gameName = self._win.getGameName()
        # 1 startingMoney = self._win.getStartingAmount()
        # 2 currency = self._win.getCurrency()
        # 3 bigBlind = self._win.getBigBlind()
        # 4 blindInterval = self._win.getBlindInterval()
        # tpl = (gameName, startingMoney, currency, bigBlind, blindInterval)
        for player in range(MAX_CLIENTS):
            self.server_data[PS][player][PS_MoneyAvailable] = rules[1]
            self.server_data[PS][player][PS_MoneyBoughtIn] = rules[1]
        self.server_data[DL][DL_GameName] = str(rules[0])
        self.server_data[DL][DL_Currency] = str(rules[2])
        self.server_data[DL][DL_BigBlind] = float(rules[3])
