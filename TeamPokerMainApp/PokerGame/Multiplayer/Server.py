from TeamPokerMainApp.Common.VariableDefinitions import *
from _thread import *
import socket
import json

# server = "192.168.0.114"
# port = 5555


class MultiplayerServerClass:

    def __init__(self, ip, port, packet):
        self.serverData = packet
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.bind((ip, port))
        except socket.error as e:
            str(e)
        self.s.listen(NO_OF_CLIENTS)
        print("Server Started... Waiting for a connection")
        start_new_thread(self.start_server_listening_loop, ())

    def start_server_listening_loop(self):
        currentPlayer = 0
        while True:
            conn, addr = self.s.accept()
            print("Connected to:", addr)
            start_new_thread(self.threaded_client_comm, (conn, currentPlayer))
            currentPlayer += 1

    def threaded_client_comm(self, conn, playerNumber):
        # Handshake Sent Message:
        conn.send(str(playerNumber).encode())
        while True:
            triesToWaitForDisconnection = 0
            try:
                # Client sent new data
                # this is done with byte-like data
                clientData = self.string_to_dict(conn.recv(BUFFERSIZE).decode())
                print(f"Server Received from Player{playerNumber}: {clientData}")

                if not clientData:
                    if triesToWaitForDisconnection > 50:
                        print("Disconnected")
                        break
                    triesToWaitForDisconnection += 1
                else:
                    #self.update_network_data_from_players(clientData, playerNumber)
                    triesToWaitForDisconnection = 0
                print(f"Server sending update to Player{playerNumber}.")
                conn.sendall(self.dict_to_string(self.serverData).encode())
            except Exception as e:
                print(f"threaded_client_comm: {e}")
                break
        print("Lost connection")
        conn.close()

    def update_network_data_from_players(self, clientData, player):
        if player > 0:
            # (status, name, iconID, money_available, actionID, [NO_CARD, NO_CARD]
            oldData = list(self.serverData["Players"][player])
            for i in range(5):  # first 5 elements of the tuple get updated by the players
                oldData[i] = clientData[i]
            self.serverData["Players"][player] = tuple(oldData)

    def update_network_data_from_dealer(self, array_table_cards, int_burned_cards, float_table_pot, dict_player_cards):
        self.serverData["TableCards"] = array_table_cards
        self.serverData["BurnedCards"] = int_burned_cards
        self.serverData["TablePot"] = float_table_pot
        for player in range(NO_OF_CLIENTS):
            oldData = list(self.serverData["Players"][player])
            oldData[player][6] = dict_player_cards[player]
            self.serverData["Players"][player] = tuple(oldData)

    def dict_to_string(self, dict):
        newDict = json.dumps(dict)
        type(f'dict_to_string Type: {newDict}')
        return newDict

    def string_to_dict(self, string):
        newDict = json.loads(string)
        type(f'string_to_dict Type: {newDict}')
        return newDict

