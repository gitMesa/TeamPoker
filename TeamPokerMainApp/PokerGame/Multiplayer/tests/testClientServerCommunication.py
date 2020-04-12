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

clientDpos = clientD.connect_to_server_and_get_position()
client1pos = client1.connect_to_server_and_get_position()
client2pos = client2.connect_to_server_and_get_position()

dealer_data = dict.copy(GAME_DATA_PACKET)
game_data1 = dict.copy(GAME_DATA_PACKET)
game_data2 = dict.copy(GAME_DATA_PACKET)


def dealer_loop(dealer_data):
    while True:
        dealer_data["Dealer"]["BurnedCards"] += int(1)
        dealer_data["Dealer"]["TablePot"] += float(0.5)
        server_data = clientD.client_communicate_with_server(dealer_data)
        dealer_data["PlayersInfo"] = server_data["PlayersInfo"]
        time.sleep(0.5)


def client1_loop(game_data1):
    while True:
        game_data1["PlayersInfo"][1][PINFO_actionID] += 1
        dealer_data = client1.client_communicate_with_server(game_data1)
        if dealer_data:
            game_data1["Dealer"]["BurnedCards"] = dealer_data["Dealer"]["BurnedCards"]
            print(f'CLIENT1: Update is done? -> {game_data1["Dealer"]["BurnedCards"]} == {dealer_data["Dealer"]["BurnedCards"]} > {game_data1["Dealer"]["BurnedCards"] == dealer_data["Dealer"]["BurnedCards"]}')
        time.sleep(1)


def client2_loop(game_data2):
    while True:
        game_data2["PlayersInfo"][2][PINFO_actionID] += 1
        dealer_data = client1.client_communicate_with_server(game_data2)
        if dealer_data:
            game_data2["Dealer"]["TablePot"] = dealer_data["Dealer"]["TablePot"]
            print(f'CLIENT2: Update is done? -> {game_data2["Dealer"]["TablePot"]} == {dealer_data["Dealer"]["TablePot"]} > {game_data2["Dealer"]["TablePot"] == dealer_data["Dealer"]["TablePot"]}')
        time.sleep(2)


try:
    threadDealer = threading.Thread(target=dealer_loop, args=(dealer_data, ))
    threadDealer.start()
except Exception as e:
    print(f'threadDealer -> {e}')

try:
    threadClient1 = threading.Thread(target=client1_loop, args=(game_data1, ))
    threadClient1.start()
except Exception as e:
    print(f'threadClient1 -> {e}')

try:
    threadClient2 = threading.Thread(target=client2_loop, args=(game_data2, ))
    threadClient2.start()
except Exception as e:
    print(f'threadClient2 -> {e}')
