from TeamPokerMainApp.Common.VariableDefinitions import *
from _thread import *
import socket


class MultiplayerServerClass:

    def __init__(self, ip, port):
        self.conn_player_number = 0
        self.conn_players_status = [0 for x in range(MAX_CLIENTS)]
        self.conn_players_adresses = [0 for x in range(MAX_CLIENTS)]
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.bind((ip, port))
        except socket.error as e:
            str(e)
        self.s.listen(MAX_CLIENTS)
        print("Server Started... Waiting for a connection")
        start_new_thread(self.server_listening_for_new_connections_loop, ())

    def server_listening_for_new_connections_loop(self):
        while True:
            conn, addr = self.s.accept()
            # save the connected player info
            self.conn_players_adresses[self.conn_player_number] = addr
            self.conn_players_status[self.conn_player_number] = STATUS_CONNECTED
            if self.conn_player_number == 0:
                print(f'SERVER: Dealer Connection Established. {self.conn_players_adresses[DEALER]} is the Dealer')
            else:
                print(f'SERVER: Client Connection Established. Client from {self.conn_players_adresses[self.conn_player_number]} is Player {self.conn_players_status[self.conn_player_number]}')
            # normally the player 0 will be the dealer that the server-mode created, which handles connection a bit differently.
            start_new_thread(self.server_communication_loop, (conn, self.conn_player_number))
            self.conn_player_number += 1

    def server_communication_loop(self, conn, clientNo):
        # Handshake Sent Message:
        conn.send(str(clientNo).encode())
        tries = 0
        while True:
            try:
                # Client sent new data this is done with byte-like data
                receivedData = conn.recv(BUFFERSIZE).decode()
                # print(f'SERVER: {type(receivedData)} -> {receivedData}')

                if not receivedData:
                    # print(f"SERVER: No data received from Client{clientNo}@{self.conn_players_adresses}. Waiting {tries}/50 tries.")
                    # tries += 1
                    # if tries > 50:
                    #     self.conn_players_status[clientNo] = STATUS_DISCONNECTED
                    #     break
                    pass
                else:
                    tries = 0
                    # if the one that is sending the message to the server is the Dealer, forward the message to the connected Clients
                    if clientNo == DEALER:
                        for player in range(1, self.conn_player_number):
                            if self.conn_players_status[clientNo] == STATUS_CONNECTED:
                                print(f"SERVER: Sending dealer update to C{player}.")
                                conn.sendto(receivedData.encode(), self.conn_players_adresses[player])
                    # if the one who is sending the message to the server is a Client, forward that message to the Dealer
                    else:
                        conn.sendto(receivedData.encode(), self.conn_players_adresses[DEALER])
            except Exception as e:
                print(f"ERROR: server_communication_loop: {e}")
                break
        print("Lost connection")
        conn.close()
