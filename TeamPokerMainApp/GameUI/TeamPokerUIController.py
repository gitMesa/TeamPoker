from TeamPokerMainApp.GameUI.TeamPokerUiStyleSheets import *
from TeamPokerMainApp.Common.VariableDefinitions import *
from TeamPokerMainApp.Common.MethodDefinitions import *
from TeamPokerMainApp.GameUI.TeamPokerUI import *
from PyQt5.Qt import QDoubleValidator

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
        self.line_starting_ammount.setValidator(QDoubleValidator(0.0, 100.0, 2))
        self.tabWidget_client_window.setCurrentIndex(0)
        self.line_host_game_ip.setText(get_ip())
        self.line_host_game_port.setText(str(5555))
        self.setServerControls(False)
        self.init_connects()

        self.player_action_array = [False, False, False, True]  # will hold which of the 3 actions player has selected (CALL, RAISE, FOLD, UNDECIDED)

    def init_connects(self):
        self.buttonHostAGame.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_HOST_A_GAME))
        self.buttonJoinAGame.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_JOIN_A_GAME))
        self.button_client_to_main_page.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_MAIN))
        self.button_host_to_main_page.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_MAIN))
        self.action_call.clicked.connect(lambda f: self.set_player_action_array(True, False, False, False))
        self.action_raise.clicked.connect(lambda f: self.set_player_action_array(False, True, False, False))
        self.action_fold.clicked.connect(lambda f: self.set_player_action_array(False, False, True, False))

    def showMainWindow(self):
        self.show()

    def goToPlayingArena(self):
        self.stackedWidget.setCurrentIndex(PAGE_PLAYING_ARENA)

    # ##### SETTERS ################################################################################################

    def setServerControls(self, bool):
        self.tab_server_settings.setEnabled(bool)
        self.button_serverStartGame.setEnabled(bool)
        self.button_serverPauseGame.setEnabled(bool)
        self.button_serverEndGame.setEnabled(bool)

    def set_player_action_array(self, call_bool, raise_bool, fold_bool, undecided_bool):
        self.player_action_array = [call_bool, raise_bool, fold_bool, undecided_bool]
        self.action_call.setChecked(call_bool)
        self.action_raise.setChecked(raise_bool)
        self.action_fold.setChecked(fold_bool)

    def setActionButtonsEnabled(self, bool):
        self.action_call.setEnabled(bool)
        self.action_raise.setEnabled(bool)
        self.action_fold.setEnabled(bool)

    def setGameStatusText(self, text):
        self.label_game_status_text.setText(str(text))

    def setNewPotValue(self, amount, currency):
        self.label_potValue.setText(f'{amount} {currency}')

    def setActionCallMoneyAmmount(self, ammount, currency):
        self.action_call.setText(f'Call {ammount} {currency}')

    def setActionRaiseMoneyAmmount(self, ammount, currency):
        self.action_raise.setText(f'Raise {ammount} {currency}')

    def setRaiseScrollBarValues(self, min, max):
        self.horizontalSlider.setMinimum(min)
        self.horizontalSlider.setMaximum(max)

    def setUiHiddenPlayer(self, pos, hidden):
        eval(f'self.player{pos}_name.setHidden(hidden)')
        eval(f'self.player{pos}_status.setHidden(hidden)')
        eval(f'self.player{pos}_money_available.setHidden(hidden)')

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

    def setUiPlayerMoneyCurrency(self, ui_pos, amount, currency):
        text = f'{amount} {currency}'
        eval(f"self.player{ui_pos}_money_available.setText(text)")

    def setUiPlayerName(self, ui_pos, name):
        eval(f'self.player{ui_pos}_name.setText(name)')

    def setUiPlayerIcons(self, ui_pos, icon_name):
        playerIcon = QtGui.QIcon(QtGui.QPixmap(f":/user_icons/user_icons/{icon_name}"))
        eval(f'self.player{ui_pos}_icon.setIcon(playerIcon)')

    def setUiPlayerActions(self, ui_pos, action_text):
        eval(f'self.player{ui_pos}_action.setText(str(action_text))')

    def setUiDealerIcons(self, ui_pos, dealer_icon_name):
        # dealer_icon_name should be ''/'dealer'/'small_blind'/'big_blind'
        if len(dealer_icon_name) > 0:
            dealer_blind_icon = QtGui.QIcon(QtGui.QPixmap(f':/other_icons/other_icons/icon_{dealer_icon_name}.png'))
        else:
            dealer_blind_icon = QtGui.QIcon(QtGui.QPixmap(''))  # if player is none of the above
        eval(f'self.player{ui_pos}_dealer.setIcon(dealer_blind_icon)')

    def updateSitOutOrPlayingText(self):
        if self.action_sit_out.isChecked():
            self.action_sit_out.setText('Sitting Out')
        else:
            self.action_sit_out.setText('Sit Out Next Turn')

    # ##### GETTERS ################################################################################################

    def getPlayerAction(self):
        return self.player_action_array.index(True)

    def getPlayerPlayingOrSittingOut(self):
        if self.action_sit_out.isChecked():
            return STATUS_PLAYER_SIT_OUT_TURN
        else:
            return STATUS_PLAYER_PLAYING

    def getUserName(self):
        return self.line_user_name.text()

    def getIconID(self):
        iconID = self.combobox_icon_selection.currentText()
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

    def getActionSitOutOrPlaying(self):
        return self.action_sit_out.isChecked()

    # ##### CONNECTs ################################################################################################

    def connectStartHostingGameServer(self, callback_function):
        self.buttonStartHostingAGame.clicked.connect(callback_function)

    def connectStartJoiningAGameServer(self, callback_function):
        self.buttonStartJoiningAGame.clicked.connect(callback_function)

    def connectButtonServerStartGame(self, callback_function):
        self.button_serverStartGame.clicked.connect(callback_function)

    def connectButtonServerPauseGame(self, callback_function):
        self.button_serverPauseGame.clicked.connect(callback_function)

    def connectButtonServerEndGame(self, callback_function):
        self.button_serverEndGame.clicked.connect(callback_function)

    def connectActionSitOut(self, callback_function):
        self.action_sit_out.clicked.connect(callback_function)

    def connectRaiseSliderMove(self, callback_function):
        self.horizontalSlider.sliderReleased.connect(callback_function)
