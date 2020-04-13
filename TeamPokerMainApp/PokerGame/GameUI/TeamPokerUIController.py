from TeamPokerMainApp.PokerGame.GameUI.TeamPokerUiStyleSheets import *
from TeamPokerMainApp.PokerGame.GameUI.TeamPokerUI import *
from PyQt5.Qt import QDoubleValidator
import socket

PAGE_MAIN = 0
PAGE_HOST_A_GAME = 1
PAGE_JOIN_A_GAME = 2
PAGE_PLAYING_ARENA = 3


class TeamPokerUIControllerClass(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(TeamPokerUIControllerClass, self).__init__(parent)
        self.setupUi(self)
        self.setStyleSheet(WINDOW_STYLE)
        self.stackedWidget.setCurrentIndex(PAGE_MAIN)
        self.buttonHostAGame.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_HOST_A_GAME))
        self.buttonJoinAGame.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_JOIN_A_GAME))
        self.button_test_play_arena.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_PLAYING_ARENA))
        self.button_client_to_main_page.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_MAIN))
        self.button_host_to_main_page.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_MAIN))
        self.button_dev_play_arena_to_main_page.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_MAIN))
        self.line_starting_ammount.setValidator(QDoubleValidator(0.0, 100.0, 2))
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

    def goToPlayingArena(self):
        self.stackedWidget.setCurrentIndex(PAGE_PLAYING_ARENA)

    # ##### SETTERS ################################################################################################

    def setUiEgoPlayerCards(self, card_number, card_code):
        if card_code == 99:
            qtIcon = QtGui.QIcon(QtGui.QPixmap(f':/cards/cards_jpeg/{card_code}_red.jpg'))
        else:
            qtIcon = QtGui.QIcon(QtGui.QPixmap(f':/cards/cards_jpeg/{card_code}.jpg'))
        if card_number is 0:
            self.player0_card1.setIcon(qtIcon)
        elif card_number is 1:
            self.player0_card2.setIcon(qtIcon)

    def setUiTableCard(self, card_number, card_code):
        if card_code == 99:
            qtIcon = QtGui.QIcon(QtGui.QPixmap(f':/cards/cards_jpeg/{card_code}_red.jpg'))
        else:
            qtIcon = QtGui.QIcon(QtGui.QPixmap(f':/cards/cards_jpeg/{card_code}.jpg'))
        eval(f"self.cards_tableCard{card_number}.setIcon(qtIcon)")

    def setUiOtherPlayersCards(self, ui_pos):
        eval(f"self.player{ui_pos}_card1.setIcon(QtGui.QIcon(QtGui.QPixmap(':/cards/cards_jpeg/99_red.jpg')))")
        eval(f"self.player{ui_pos}_card2.setIcon(QtGui.QIcon(QtGui.QPixmap(':/cards/cards_jpeg/99_red.jpg')))")

    def setUiPlayerMoneyCurrency(self, ui_pos, ammount):
        eval(f'self.player{ui_pos}_money_available.setText(str(ammount))')

    def setUiPlayerName(self, ui_pos, name):
        eval(f'self.player{ui_pos}_name.setText(name)')

    def setUiPlayerIcons(self, ui_pos, icon_name):
        playerIcon = QtGui.QIcon(QtGui.QPixmap(f":/user_icons/user_icons/{icon_name}"))
        eval(f'self.player{ui_pos}_icon.setIcon(playerIcon)')

    def setUiPlayerActions(self, ui_pos, action):
        eval(f'self.player{ui_pos}_action.setText(str(action))')

    def setUiDealerIcons(self, ui_pos, dealer_icon_name):
        # dealer_icon_name should be ''/'dealer'/'small_blind'/'big_blind'
        if len(dealer_icon_name) > 0:
            dealer_blind_icon = QtGui.QIcon(QtGui.QPixmap(f':/other_icons/other_icons/icon_{dealer_icon_name}.png'))
        else:
            dealer_blind_icon = QtGui.QIcon(QtGui.QPixmap(''))  # if player is none of the above
        eval(f'self.player{ui_pos}_dealer.setIcon(dealer_blind_icon)')

    # ##### GETTERS ################################################################################################

    def getUserAction(self):
        return None

    def getUserName(self):
        return self.line_user_name.text()

    def getIconID(self):
        iconID = self.icon_selection_combobox.currentText()
        return iconID

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

    def connectStartHostingGameServer(self, callback_function):
        self.buttonStartHostingAGame.clicked.connect(callback_function)

    def connectStartJoiningAGameServer(self, callback_function):
        self.buttonStartJoiningAGame.clicked.connect(callback_function)

    def connectButtonDevStartDealer(self, callback_function):
        self.button_dev_start_dealing.clicked.connect(callback_function)
