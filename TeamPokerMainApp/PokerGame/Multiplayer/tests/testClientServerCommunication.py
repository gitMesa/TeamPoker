from TeamPokerMainApp.PokerGame.Multiplayer.Server import MultiplayerServerClass
from TeamPokerMainApp.PokerGame.Multiplayer.Client import ClientClass
from PyQt5.Qt import QMutex
import socket
import time


ip = socket.gethostbyname(socket.gethostname())
port = 55555

GAME_DATA_PACKET = {"TableCards": [0, 0, 0, 0, 0],
                    "BurnedCards": int(0),
                    "TablePot": float(0.0),
                    1: (int(0), int(0), str(""), int(0), int(0), float(0.0), str(""), [0, 0]),
                    2: (int(0), int(0), str(""), int(0), int(0), float(0.0), str(""), [0, 0])
                    }

srv = MultiplayerServerClass(ip, port)
mutex = QMutex()

client1 = ClientClass(ip, port)
client2 = ClientClass(ip, port)

client1pos = client1.connect_to_server_and_get_player_position()
client2pos = client2.connect_to_server_and_get_player_position()

print(f'Client1pos = {client1pos} & Client2pos = {client2pos}')

while True:
    print(f'C1 Sending.')
    while True:  # try to access the GAME_DATA_PACKET
        if mutex.tryLock():  # if access is successful
            game_data = GAME_DATA_PACKET
            game_data["BurnedCards"] += int(1)
            rtrn1 = client1.send_client_data_and_receive_dealer_data(game_data)
            mutex.unlock()
            break
    print(f'C1 Received {rtrn1}')

    print(f'C2 Sending.')
    while True:  # try to access the GAME_DATA_PACKET
        if mutex.tryLock():  # if access is successful
            game_data = GAME_DATA_PACKET
            game_data["TablePot"] += float(1.0)
            rtrn2 = client2.send_client_data_and_receive_dealer_data(GAME_DATA_PACKET)
            mutex.unlock()
            break
    print(f'C2 Received {rtrn2}')
    time.sleep(1)

