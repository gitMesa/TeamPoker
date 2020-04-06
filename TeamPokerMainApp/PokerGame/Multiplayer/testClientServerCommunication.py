from TeamPokerMainApp.PokerGame.Multiplayer.Server import MultiplayerServerClass
from TeamPokerMainApp.PokerGame.Multiplayer.Client import ClientClass
import socket
import time


ip = socket.gethostbyname(socket.gethostname())
port = 55555

srv = MultiplayerServerClass(ip, port)

client1 = ClientClass(ip, port)
client2 = ClientClass(ip, port)


while True:
    rtrn1 = client1.send_and_receive_update()
    rtrn2 = client2.send_and_receive_update()
    print(f'reply1 = {rtrn1} and reply2 = {rtrn2}')
    time.sleep(3)
