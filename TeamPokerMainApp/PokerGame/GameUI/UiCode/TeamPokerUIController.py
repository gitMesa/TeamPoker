from TeamPokerMainApp.PokerGame.GameUI.UiCode.TeamPokerUI import *
from PyQt5.Qt import QDoubleValidator, QIntValidator
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
        self.button_dev_play_arena_to_main_page.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_MAIN))
        self.line_host_game_ip.setText(self.get_ip())
        self.line_host_game_port.setText(str(5555))
        self.line_starting_ammount.setValidator(QDoubleValidator(0.0, 100.0, 2))

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

    def goToPlayingArena(self):
        self.stackedWidget.setCurrentIndex(PAGE_PLAYING_ARENA)

    # ##### SETTERS ################################################################################################

    def setUiEgoPlayerCards(self, card_number, card_code):
        qtIcon = QtGui.QIcon(QtGui.QPixmap(f'url(:/cards/cards_jpeg/{card_code}.jpg)'))
        if card_number is 1:
            self.playerEGO_card1.setIcon(qtIcon)
        elif card_number is 2:
            self.playerEGO_card2.setIcon(qtIcon)

    def setUiPlayerMoneyCurrency(self, player, ammount):
        eval(f'self.player{player}_money_available.setText(ammount)')

    def setUiPlayerName(self, player, name):
        eval(f'self.player{player}_name.setText(name)')

    def setUiPlayerIcons(self, player, icon_name):
        playerIcon = QtGui.QIcon(QtGui.QPixmap(f'url(:/user_icons/user_icons/icons8-{icon_name}-70.png)'))
        eval(f'self.player{player}_icon.setIcon(playerIcon)')

    def setUiDealerIcons(self, player, dealer_icon_name):
        # dealer_icon_name should be 'dealer'/'small_blind'/'big_blind'
        if len(dealer_icon_name) > 0:
            dealer_blind_icon = QtGui.QIcon(QtGui.QPixmap(f'url(:/other_icons/other_icons/icon_{dealer_icon_name}.png)'))
        else:
            dealer_blind_icon = ''  # if player is none of the above
        eval(f'self.player{player}_dealer.setIcon(dealer_blind_icon)')

    # ##### GETTERS ################################################################################################

    def getUserName(self):
        return self.line_user_name.text()

    def getIconID(self):
        return self.icon_selection_combobox.currentText()

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
        if len(self.line_starting_ammount.text()) > 0:
            return float(self.line_starting_ammount.text())
        else:
            return 0

    def getCurrency(self):
        return self.line_currency.text()

    def getSmallBlind(self):
        return float(self.spinbox_small_blind.value())

    def getBigBlind(self):
        return float(self.spinbox_big_blind.value())

    def getBlindInterval(self):
        return self.combobox_blind_raise_interval.currentText()

    def connectButtonHostGame(self, callback_function):
        self.buttonStartHostingAGame.clicked.connect(callback_function)

    def connectButtonJoinGame(self, callback_function):
        self.buttonJoinAGame.clicked.connect(callback_function)

    def connectButtonDevStartDealer(self, callback_function):
        self.button_dev_start_dealing.clicked.connect(callback_function)
