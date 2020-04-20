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

def dict_to_string(dictionary):
    return str(dictionary)

def string_to_dict(string):
    return eval(string)

