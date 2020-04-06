from TeamPokerMainApp.PokerGame.GameUI.UiCode.TeamPokerUI import *
import socket

PAGE_MAIN = 0
PAGE_HOST_A_GAME = 1
PAGE_JOIN_A_GAME = 2
PAGE_PLAYING_ARENA = 3


class TeamPokerUIControllerClass(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(TeamPokerUIControllerClass, self).__init__(parent)
        self.setupUi(self)
        self.stackedWidget.setCurrentIndex(PAGE_MAIN)
        self.buttonHostAGame.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_HOST_A_GAME))
        self.buttonJoinAGame.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_JOIN_A_GAME))
        self.button_test_play_arena.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_PLAYING_ARENA))
        self.button_client_to_main_page.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_MAIN))
        self.button_host_to_main_page.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_MAIN))
        self.button_play_arena_to_main_page.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_MAIN))
        self.line_host_game_ip.setText(self.get_ip())
        self.line_host_game_port.setText(str(5555))

    def get_ip(self):
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

    def showMainWindow(self):
        self.show()

    def getGameName(self):
        return self.line_game_name.text()

    def getHostAGameIpAdress(self):
        return self.line_host_game_ip.text()

    def getJoinAGameIpAdress(self):
        return self.line_join_game_ip.text()

    def getHostAGamePortNumber(self):
        return int(self.line_host_game_port.text())

    def getJoinAGamePortNumber(self):
        return int(self.line_join_game_port.text())

    def getStartingAmmount(self):
        return float(self.line_starting_ammount.text())

    def getCurrency(self):
        return self.line_currency.text()

    def getSmallBlind(self):
        return float(self.spinbox_small_blind.text())

    def getBigBlind(self):
        return float(self.spinbox_big_blind.text())

    def getBlindInterval(self):
        return self.combobox_blind_raise_interval.currentText()

    def connectButtonHostGame(self, callback_function):
        self.buttonStartHostingAGame.clicked.connect(callback_function)

    def connectButtonJoinGame(self, callback_function):
        self.buttonJoinAGame.clicked.connect(callback_function)
