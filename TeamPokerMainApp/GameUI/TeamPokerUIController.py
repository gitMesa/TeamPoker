from TeamPokerMainApp.GameUI.TeamPokerUiStyleSheets import *
from TeamPokerMainApp.Common.MethodDefinitions import *
from TeamPokerMainApp.GameUI.TeamPokerUI import *
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.Qt import QDoubleValidator, QAbstractItemView
from PyQt5.QtCore import Qt


PAGE_MAIN = 0
PAGE_HOST_A_GAME = 1
PAGE_JOIN_A_GAME = 2
PAGE_PLAYING_ARENA = 3


class TeamPokerUIControllerClass(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(TeamPokerUIControllerClass, self).__init__(parent)
        self.setupUi(self)
        self.setStyleSheet(WINDOW_STYLE)
        self.line_starting_ammount.setValidator(QDoubleValidator(0.0, 100.0, 2))
        self.line_raise_amount.setValidator(QDoubleValidator(0.0, 100.0, 2))
        self.stackedWidget.setCurrentIndex(PAGE_MAIN)
        self.tabWidget_client_window.setCurrentIndex(0)
        self.line_host_game_ip.setText(get_ip())  # TODO: remove
        self.line_host_game_port.setText(str(5555))  # TODO: remove
        self.table_money_stats.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_player_server_statuses.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.listView.setModel(QStandardItemModel())
        self.setServerControls(False)
        self.init_connects()

        self.player_action_array = [False, False, False, True]  # will hold which of the 3 actions player has selected (CALL, RAISE, FOLD, UNDECIDED)
        self.history_rows = -1  # in order to put first row at index 0

    def init_connects(self):
        self.buttonHostAGame.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_HOST_A_GAME))
        self.buttonJoinAGame.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_JOIN_A_GAME))
        self.button_client_to_main_page.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_MAIN))
        self.button_host_to_main_page.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_MAIN))
        self.action_call.clicked.connect(lambda f: self.set_player_action_array(True, False, False, False))
        self.action_raise.clicked.connect(lambda f: self.set_player_action_array(False, True, False, False))
        self.action_fold.clicked.connect(lambda f: self.set_player_action_array(False, False, True, False))
        self.spinbox_big_blind.valueChanged.connect(self.setSmallBlindText)

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

    def reset_player_action_array(self):
        self.set_player_action_array(False, False, False, True)

    def setActionButtonsEnabled(self, bool):
        self.action_call.setEnabled(bool)
        self.action_raise.setEnabled(bool)
        self.action_fold.setEnabled(bool)

    def setTableCenterText(self, text):
        self.label_game_status_text.setText(str(text))

    def setNewPotValue(self, amount, currency):
        self.label_potValue.setText(f'{amount} {currency}')

    def setActionCallMoneyAmmount(self, amount, currency):
        self.action_call.setText(f'Call {amount} {currency}')

    def setActionRaiseMoneyAmount(self, amount, currency):
        self.action_raise.setText(f'Raise {amount} {currency}')
        self.line_raise_amount.setText(f'{amount}')

    def setRaiseScrollBarValues(self, min, max, step):
        self.horizontalSlider.setSingleStep(step)
        self.horizontalSlider.setMinimum(min)
        self.horizontalSlider.setMaximum(max)

    def setUiHiddenPlayer(self, pos, hidden):
        eval(f'self.player{pos}_name.setHidden(hidden)')
        eval(f'self.player{pos}_status.setHidden(hidden)')
        eval(f'self.player{pos}_money_available.setHidden(hidden)')

    def setUiEgoPlayerCards(self, card_number, card_name):
        qtIcon = QtGui.QIcon(QtGui.QPixmap(f':/cards/cards_jpeg/{card_name}.jpg'))
        if card_number is 0:
            self.player0_card1.setIcon(qtIcon)
        elif card_number is 1:
            self.player0_card2.setIcon(qtIcon)

    def setUiBurnedCards(self, number_of_burned_cards):
        if number_of_burned_cards > 0:
            qtIcon = QtGui.QIcon(QtGui.QPixmap(f':/cards/cards_jpeg/burned_{number_of_burned_cards}.jpg'))
            self.cards_burnedCards.setIcon(qtIcon)
        else:
            self.cards_burnedCards.setIcon(QtGui.QIcon(QtGui.QPixmap('')))

    def setUiTableCard(self, card_number, card_name):
        qtIcon = QtGui.QIcon(QtGui.QPixmap(f':/cards/cards_jpeg/{card_name}.jpg'))
        if '99' in card_name:
            qtIcon = QtGui.QIcon(QtGui.QPixmap(''))
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

    def setUiPlayerActions(self, ui_pos, status_text):
        eval(f'self.player{ui_pos}_status.setText(str(status_text))')

    def setUiDealerIcons(self, ui_pos, dealer_icon_name):
        # dealer_icon_name should be '' or 'dealer' or 'small_blind' or 'big_blind'
        if len(dealer_icon_name) > 0:
            dealer_blind_icon = QtGui.QIcon(QtGui.QPixmap(f':/other_icons/other_icons/icon_{dealer_icon_name}.png'))
        else:
            dealer_blind_icon = QtGui.QIcon(QtGui.QPixmap(''))  # if player is none of the above
        eval(f'self.player{ui_pos}_dealer.setIcon(dealer_blind_icon)')

    def setUiPlayerConnStatuses(self, row, name, stat_text):
        column_name, column_stat = 0, 1
        self.table_player_server_statuses.setItem(row, column_name, QTableWidgetItem(name))
        self.table_player_server_statuses.setItem(row, column_stat, QTableWidgetItem(stat_text))

    def setUiPlayerMoneyStatuses(self, row, name, money_in, money_left):
        col_name, col_money_in, col_money_left, col_delta = 0, 1, 2, 3
        delta = money_in - money_left
        # add text centered
        item_name = QTableWidgetItem(name)
        item_name.setTextAlignment(Qt.AlignHCenter)
        self.table_money_stats.setItem(row, col_name, item_name)
        # add text centered
        item_money_in = QTableWidgetItem(str(float(money_in)))
        item_money_in.setTextAlignment(Qt.AlignHCenter)
        self.table_money_stats.setItem(row, col_money_in, item_money_in)
        # add text centered
        item_money_left = QTableWidgetItem(str(float(money_left)))
        item_money_left.setTextAlignment(Qt.AlignHCenter)
        self.table_money_stats.setItem(row, col_money_left, item_money_left)
        # add text centered
        item_delta = QTableWidgetItem(str(delta))
        item_delta.setTextAlignment(Qt.AlignHCenter)
        self.table_money_stats.setItem(row, col_delta, item_delta)

    def setNewTextItemToUiTableHistory(self, text):
        self.listView.model().appendRow(QStandardItem(text))
        self.history_rows += 1

    def setSmallBlindText(self):
        bigblind = self.spinbox_big_blind.value()
        self.line_small_blind.setText(str(float(bigblind)/2))

    def togglePlayOrSitOutButtonText(self):
        if self.action_play_or_sit_out.isChecked():
            self.action_play_or_sit_out.setText('Resume Playing')
        else:
            self.action_play_or_sit_out.setText('Sit Out Next Turn')

    # ##### GETTERS ################################################################################################

    def getUiTableHistoryRowNumber(self):
        return self.history_rows

    def getUiTableHistoryLastRowText(self):
        if self.history_rows >= 0:
            return self.listView.model().index(self.history_rows, 0).data()
        else:
            return ''

    def getPlayerAction(self):
        return self.player_action_array.index(True)

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

    def getBigBlind(self):
        return float(self.spinbox_big_blind.value())

    def getBlindInterval(self):
        return self.combobox_blind_raise_interval.currentText()

    def getActionPlayOrSitOut(self):
        return self.action_play_or_sit_out.isChecked()

    def getRaiseSliderValue(self):
        return float(self.horizontalSlider.value())

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
        self.action_play_or_sit_out.clicked.connect(callback_function)

    def connectActionBuyIn(self, callback_function):
        self.action_buy_in.clicked.connect(callback_function)

    def connectRaiseSliderChanged(self, callback_function):
        self.horizontalSlider.valueChanged.connect(callback_function)
