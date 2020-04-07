from PyQt5.QtWidgets import QErrorMessage, QMessageBox

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
