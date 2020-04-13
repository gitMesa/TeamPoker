from TeamPokerMainApp.PokerGame.Multiplayer.NetworkPacket import NetworkPacketClass
from TeamPokerMainApp.PokerGame.Multiplayer.Server import MultiplayerServerClass
from TeamPokerMainApp.PokerGame.Multiplayer.Client import ClientClass
from TeamPokerMainApp.Common.VariableDefinitions import *
import threading
import socket
import time

ip = socket.gethostbyname(socket.gethostname())
port = 55555

packet = NetworkPacketClass()
GAME_DATA_PACKET = dict.copy(packet.get_game_data())

srv = MultiplayerServerClass(ip, port)

clientD = ClientClass(ip, port)
client1 = ClientClass(ip, port)
client2 = ClientClass(ip, port)

clientDpos = int(clientD.connect_to_server_and_get_position())
client1pos = int(client1.connect_to_server_and_get_position())
client2pos = int(client2.connect_to_server_and_get_position())

print(f'Dealer {clientDpos} Client1 {client1pos} Client2 {client2pos}')

dealer_data = dict.copy(GAME_DATA_PACKET)
game_data1 = dict.copy(GAME_DATA_PACKET)
game_data2 = dict.copy(GAME_DATA_PACKET)


def dealer_loop():
    while True:
        dealer_data["Dealer"]["BurnedCards"] += int(1)
        dealer_data["Dealer"]["TablePot"] += float(0.5)
        server_data = clientD.client_communicate_with_server(dealer_data)
        dealer_data["PlayersInfo"] = server_data["PlayersInfo"]
        print(f'Client Updates: {dealer_data["PlayersInfo"]}')
        time.sleep(0.5)


def client1_loop():
    while True:
        game_data1["PlayersInfo"][client1pos][PINFO_actionID] += 1
        dealer_data = client1.client_communicate_with_server(game_data1)
        if dealer_data:
            game_data1["Dealer"]["BurnedCards"] = dealer_data["Dealer"]["BurnedCards"]
            print(f'CLIENT1: Update is done? -> {game_data1["Dealer"]["BurnedCards"]} == {dealer_data["Dealer"]["BurnedCards"]} > {game_data1["Dealer"]["BurnedCards"] == dealer_data["Dealer"]["BurnedCards"]}')
        time.sleep(1)


def client2_loop():
    while True:
        game_data2["PlayersInfo"][client2pos][PINFO_actionID] += 1
        dealer_data = client2.client_communicate_with_server(game_data2)
        if dealer_data:
            game_data2["Dealer"]["BurnedCards"] = dealer_data["Dealer"]["BurnedCards"]
            print(f'CLIENT1: Update is done? -> {game_data2["Dealer"]["BurnedCards"]} == {dealer_data["Dealer"]["BurnedCards"]} > {game_data2["Dealer"]["BurnedCards"] == dealer_data["Dealer"]["BurnedCards"]}')
        time.sleep(2)


try:
    threadDealer = threading.Thread(target=dealer_loop)
    threadDealer.start()
except Exception as e:
    print(f'threadDealer -> {e}')

try:
    pass
    threadClient1 = threading.Thread(target=client1_loop)
    threadClient1.start()
except Exception as e:
    print(f'threadClient1 -> {e}')

try:
    threadClient2 = threading.Thread(target=client2_loop)
    threadClient2.start()
except Exception as e:
    print(f'threadClient2 -> {e}')
