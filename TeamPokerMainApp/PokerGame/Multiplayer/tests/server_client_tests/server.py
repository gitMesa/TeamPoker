import threading
import socket


PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = '!DISCONNECT'

HEADER = 2048

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def start():
    server.listen(5)
    print(f"SERVER: Listening on {SERVER}. ")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f'SERVER: Active connections: {threading.activeCount() - 1}. ')


def handle_client(conn, addr):
    print(f'SERVER: New connection: {addr}')
    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False
            print(f'{addr} -> {msg}')
            conn.send("Msg received").encode(FORMAT)
    conn.close()


print('SERVER: Starting server...')
start()