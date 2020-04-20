from TeamPokerMainApp.Common.VariableDefinitions import *
from PyQt5.QtWidgets import QErrorMessage, QMessageBox
import socket


def showCustomizedErrorWindow(errorMessage):
    err = QErrorMessage()
    err.showMessage(f'Error {errorMessage}')
    err.setWindowTitle('Whoops...')
    err.exec()


def showCustomizedInfoWindow(infoMessage):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setStandardButtons(QMessageBox.Ok)
    msg.setText(infoMessage)
    msg.setWindowTitle('Hmmm...')
    msg.exec_()

############################################################################
#  Client-Server SOCKET Methods
############################################################################


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


# We send 2 messages between client-server.
# First we find the size of the dictionary we want to send, and tell the server to receive that size.
# Second we send the dictionary in string format.
def send_message_with_size_confirmation(conn, message):
    message_as_string = transform_into_string(message)
    message_as_string = message_as_string.encode(FORMAT)
    message_size = str(len(message_as_string)).encode(FORMAT)
    # Fill the message_size with empty bites until we reach the HEADER size.
    message_size += b' ' * (HEADER - len(message_size))
    # Send the HEADER with the information about the size of the dict we are about to send.
    conn.send(message_size)
    # Send the actual message.
    conn.sendall(message_as_string)


def send_simple_message(conn, message):
    message_as_string = transform_into_string(message)
    conn.send(message_as_string.encode(FORMAT))


# We send 2 messages between client-server.
# First we find the size of the dictionary we want to send, and tell the server to receive that size.
# Second we send the dictionary in string format.
def receive_message_with_size_confirmation(conn):
    message_size = int(conn.recv(HEADER).decode(FORMAT))
    client_data = conn.recv(message_size).decode(FORMAT)
    return client_data


def receive_simple_message(conn):
    message = conn.recv(HEADER).decode(FORMAT)
    return message


def transform_into_string(dictionary):
    return str(dictionary)


def transform_into_data(string):
    return eval(string)

