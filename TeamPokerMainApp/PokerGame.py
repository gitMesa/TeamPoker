from TeamPokerMainApp.Multiplayer.ClientCommunication import ClientCommunicationClass
from TeamPokerMainApp.GameUI.TeamPokerUIController import TeamPokerUIControllerClass
from TeamPokerMainApp.Multiplayer.NetworkPacket import NetworkPacketClass
from TeamPokerMainApp.Multiplayer.Server import MultiplayerServerClass
from TeamPokerMainApp.GameLogic.CardDeck import CardDeckClass
from TeamPokerMainApp.Common.NetworkPacketDefinitions import *
from TeamPokerMainApp.Common.MethodDefinitions import *
from PyQt5.QtWidgets import QInputDialog
from PyQt5.Qt import QTimer


####################################################################
# Purpose of this class is to connect the UI to the Game Logic part.
# From the UI you can either create a Server or a Client
#
# 1.Start Server.
#   Shall create a server with selected input (Starting Money, Currency, Etc.)
#   Shall connect to said server and wait for enough players.
#   Start game after enough players are connected.
#   Server receives the input information and handles the game data.
#
# 2.Client:
#   Shall connect to the server providing UserName and UserIcon?
#   Shall receive from Server game data.
#   Shall send to Server player data.
#
###################################################################


class PokerGameClass(NetworkPacketClass, CardDeckClass):

    def __init__(self):
        self._win = TeamPokerUIControllerClass()
        self.client_data = self.get_network_packet_definition()
        self.initConnectUiElements()
        self.initOtherStuff()
        self.setDevQuickLaunchSettings()

    def show_main_window(self):
        self._win.showMainWindow()

    def initConnectUiElements(self):
        self._win.connectStartHostingGameServer(self.start_poker_server)
        self._win.connectStartJoiningAGameServer(self.join_poker_server)
        self._win.connectButtonServerStartGame(lambda f: self.change_game_status_on_server(Overwrite_START_GAME))
        self._win.connectButtonServerPauseGame(lambda f: self.change_game_status_on_server(Overwrite_PAUSE_GAME))
        self._win.connectButtonServerEndGame(lambda f: self.change_game_status_on_server(Overwrite_END_GAME))
        self._win.connectRaiseSliderMoved(self.set_raise_button_text)
        self._win.connectActionSitOut(self._win.togglePlayOrSitOutButtonText)
        self._win.connectActionBuyIn(self.show_buy_in_window)

    def initOtherStuff(self):
        for player in range(MAX_CLIENTS):
            self._win.setUiHiddenPlayer(player, True)

################################################################################################
# 1. Network Stuff (Client & Server):
################################################################################################

    def start_poker_server(self):
        if self.check_if_all_host_server_fields_have_input():
            try:
                ip_port = (self._win.getHostAGameIpAdress(), self._win.getHostAGamePortNumber())
                self._srv = MultiplayerServerClass(ip_port=ip_port, game_rules=self.get_game_rules())
            except Exception as e:
                print(f'ERROR: start_poker_server -> MultiplayerServerClass -> {e}')

            try:
                ip_port = (self._win.getHostAGameIpAdress(), self._win.getHostAGamePortNumber())
                self.start_network_client(ip_port)
            except Exception as e:
                print(f'ERROR: start_poker_server -> start_network_client -> {e}')

            self._win.goToPlayingArena()
            self._win.setServerControls(True)
        else:
            showCustomizedInfoWindow('Please fill all information!')

    def join_poker_server(self):
        if self.check_if_all_join_server_fields_have_input():
            try:
                ip_port = (self._win.getJoinAGameIpAdress(), self._win.getJoinAGamePortNumber())
                self.start_network_client(ip_port=ip_port)
            except Exception as e:
                showCustomizedInfoWindow(f'Could not connect to server! {e}')
                print(f'ERROR: join_poker_server -> start_network_client PLAYER -> {e}')
            self._win.goToPlayingArena()

    def start_network_client(self, ip_port):
        self._client = ClientCommunicationClass(ip_port=ip_port)
        self.client_index = int(self._client.client_connect_to_server_and_get_position())
        self.table_spots = self.get_table_spots_from_client_index_point_of_view()
        self.client_init_game_data_from_own_ui()
        self.client_server_communication_loop()

    def client_server_communication_loop(self):
        self.communication_timer = QTimer(self._win)
        self.communication_timer.start(COMMUNCATION_TIME)
        self.communication_timer.timeout.connect(self.client_server_comm_action)

    def client_server_comm_action(self):
        reply_data = None
        try:
            # update the game_data with own ui info (mainly new actions, decisions by the player)
            self.client_update_game_data_from_own_ui()
        except Exception as e:
            print(f'client_update_game_data_from_own_ui -> {e}')

        try:  # Send your user update and get the update from all other clients, and dealer, centralized by the server.
            reply_data = self._client.client_send_message_to_server_return_reply(self.client_data)
        except Exception as e:
            print(f'client_send_message_to_server_return_reply -> {e}')

        try:  # update our own UI based on the data received from the server (cards, other players, etc.)
            if reply_data:  # in case data failed to be received correctly, don't overwrite it locally.
                self.client_data = reply_data
                self.client_update_own_ui_from_new_server_data()
        except Exception as e:
            print(f'client_update_own_ui_from_new_server_data -> {e}')

######################################################################################################
# 2. Client-Ui Logic:
######################################################################################################

    def client_init_game_data_from_own_ui(self):  # INIT stuff only!!!!!
        self.client_data[PC][self.client_index][PC_TableSpot] = self.client_index
        self.client_data[PC][self.client_index][PC_Icon] = self._win.getIconID()
        self.client_data[PC][self.client_index][PC_Name] = self._win.getUserName()

    def client_update_game_data_from_own_ui(self):
        # if button is checked -> Sitting Out -> isPlayerPlaying = False
        self.client_data[PC][self.client_index][PC_isPlayerPlaying] = not self._win.getActionPlayOrSitOut()

        # Check if it's our turn to take a decision:
        if self.client_data[DL][DL_idNextDecision] == self.client_index:
            player_action = self._win.getPlayerAction()
            # if we decided copy the decision to the game_data
            if player_action is not ACTION_UNDECIDED:
                self.client_data[PC][self.client_index][PC_idPlayerAction] = player_action
        else:
            # if it's no longer our time to take a decision, reset the decision.
            self.client_data[PC][self.client_index][PC_idPlayerAction] = ACTION_UNDECIDED
            self._win.reset_player_action_array()

    def client_update_own_ui_from_new_server_data(self):
        # EACH PLAYER DATA
        for player in range(MAX_CLIENTS):
            if self.client_data[PS][player][PS_ConnectionStatus] is CONN_STATUS_CONNECTED:
                ui_pos = self.table_spots.index(player)
                player_name = self.client_data[PC][player][PC_Name]
                self._win.setUiHiddenPlayer(pos=ui_pos, hidden=False)  # Show the player table in UI
                self._win.setUiPlayerName(ui_pos=ui_pos, name=player_name)
                self._win.setUiPlayerIcons(ui_pos=ui_pos, icon_name=self.client_data[PC][player][PC_Icon])
                self.set_ui_player_dealer_icons(ui_pos=ui_pos, player=player)
                self._win.setUiPlayerMoneyCurrency(ui_pos=ui_pos, amount=self.client_data[PS][player][PS_MoneyAvailable], currency=self.client_data[DL][DL_Currency])
                self._win.setUiPlayerActions(ui_pos=ui_pos, status_text=self.client_data[PC][player][PC_textPlayerTable])
                self._win.setUiOtherPlayersCards(ui_pos)  # TODO: Show actual cards at end of round
                # Update the tabs
                self.set_ui_player_server_connection_statuses(player=player, player_name=player_name)
                self.set_ui_player_money_statuses(player=player, player_name=player_name)
            else:
                ui_pos = self.table_spots.index(player)
                self._win.setUiHiddenPlayer(pos=ui_pos, hidden=True)
        # TABLE CARDS
        table_cards = self.client_data[DL][DL_TableCards]
        for card in range(NUMBER_OF_CARDS_ON_TABLE):
            card_name = self.get_card_name_from_card_number(table_cards[card])
            self._win.setUiTableCard(card_number=card, card_name=card_name)
        # PLAYER CARDS
        player_cards = self.client_data[PS][self.client_index][PS_PlayerCards]  # returns array with card codes
        for card in range(NUMBER_OF_CARDS_IN_HAND):
            card_name = self.get_card_name_from_card_number(player_cards[card])
            self._win.setUiEgoPlayerCards(card_number=card, card_name=card_name)
        # GAME STATUSES & HISTORY
        self.add_item_to_table_history()
        self._win.setGameStatusText(text=self.client_data[DL][DL_textTableCenter])
        self._win.setNewPotValue(amount=self.client_data[DL][DL_TablePot], currency=self.client_data[DL][DL_Currency])
        self._win.setUiBurnedCards(number_of_burned_cards=self.client_data[DL][DL_noBurnedCards])
        # If it is my turn to decide, update the call/raise button texts, and enable those buttons.
        if self.client_data[DL][DL_idNextDecision] == self.client_index and not self._win.getActionPlayOrSitOut():
            self._win.setActionButtonsEnabled(True)
            self._win.setActionCallMoneyAmmount(amount=self.client_data[DL][DL_MinBet], currency=self.client_data[DL][DL_Currency])
            self.set_minimum_maximum_slider_values()
        else:
            self._win.setActionButtonsEnabled(False)
            self._win.setActionCallMoneyAmmount(amount='', currency='')
            self._win.setActionRaiseMoneyAmmount(amount='', currency='')

    def set_ui_player_dealer_icons(self, ui_pos, player):
        # There is only 1 dealer/blind icon spot. So if there are 2 players only and 1 is both dealer and big blind... fuck it.
        if self.client_data[PS][player][PS_isDealer] is TABLE_STATUS_is_DEALER:
            self._win.setUiDealerIcons(ui_pos=ui_pos, dealer_icon_name='dealer')
        elif self.client_data[PS][player][PS_isBlind] is TABLE_STATUS_is_SMALL_BLIND:
            self._win.setUiDealerIcons(ui_pos=ui_pos, dealer_icon_name='small_blind')
        elif self.client_data[PS][player][PS_isBlind] is TABLE_STATUS_is_BIG_BLIND:
            self._win.setUiDealerIcons(ui_pos=ui_pos, dealer_icon_name='big_blind')
        else:
            self._win.setUiDealerIcons(ui_pos=ui_pos, dealer_icon_name='')

    def add_item_to_table_history(self):
        last_item = self._win.getUiTableHistoryLastRowText()
        if last_item != self.client_data[DL][DL_textTableCenter] or last_item == '':
            self._win.setNewTextItemToUiTableHistory(text=self.client_data[DL][DL_textTableCenter])

    def set_ui_player_server_connection_statuses(self, player, player_name):
        stat = self.client_data[PS][player][PS_ConnectionStatus]
        if stat is CONN_STATUS_CONNECTED:
            stat_text = "Connected!"
        elif stat is CONN_STATUS_DISCONNECTED:
            stat_text = "Disconnected!"
        else:
            stat_text = "Empty seat."
        self._win.setUiPlayerConnStatuses(row=player, name=player_name, stat_text=stat_text)

    def set_ui_player_money_statuses(self, player, player_name):
        money_in = self.client_data[PS][player][PS_MoneyBoughtIn]
        money_left = self.client_data[PS][player][PS_MoneyAvailable]
        self._win.setUiPlayerMoneyStatuses(row=player, name=player_name, money_in=money_in, money_left=money_left)

    def set_minimum_maximum_slider_values(self):
        step = self.client_data[DL][DL_BigBlind]
        min_value = self.client_data[DL][DL_MinBet]
        max_value = self.client_data[PS][self.client_index][PS_MoneyAvailable]
        self._win.setRaiseScrollBarValues(min=min_value, max=max_value, step=step)

    def set_raise_button_text(self):
        self._win.setActionRaiseMoneyAmmount(amount=self._win.getRaiseSliderValue(), currency=self.client_data[DL][DL_Currency])

    def change_game_status_on_server(self, status):
        # Normally only the server should start the game. This is a workaround.
        self.client_data[PC][self.client_index][PC_ClientOverwrite] = status

######################################################################################################
# 5. Other Logic:
######################################################################################################

    def get_table_spots_from_client_index_point_of_view(self):
        ########################################################################################################################
        # This needs to be shown from my point of view. So roll everyone around the table until i am sitting in the front seat.#
        ########################################################################################################################
        #   For example the normal table is indexed like this:    #             But from player2 point-of-view:                #
        #                       player4                           #                       player6                              #
        #     player3                             player5         #     player5                             player7            #
        #  player2                                    player6     #  player4                                    player0        #
        #     player1                             player7         #     player3                             player1            #
        #                       player0                           #                       player2                              #
        ########################################################################################################################
        table_spots = [0, 1, 2, 3, 4, 5, 6, 7]
        for i in range(table_spots.index(self.client_index)):
            table_spots.append(table_spots[0])
            table_spots.remove(table_spots[0])
        return table_spots

    def get_game_rules(self):
        gameName = self._win.getGameName()
        startingMoney = self._win.getStartingAmmount()
        currency = self._win.getCurrency()
        bigBlind = self._win.getBigBlind()
        blindInterval = self._win.getBlindInterval()
        tpl = (gameName, startingMoney, currency, bigBlind, blindInterval)
        return tpl

    def check_if_all_host_server_fields_have_input(self):
        rtrn = False
        if self._win.getStartingAmmount() > 0 and len(self._win.getCurrency()) > 0 and self._win.getBigBlind() > 0:
            rtrn = True
        return rtrn

    def check_if_all_join_server_fields_have_input(self):
        rtrn = True
        # TODO: check ip & port
        return rtrn

    def show_buy_in_window(self):
        buy_in_amount, ok = QInputDialog.getDouble(None, 'Buy-In', 'Enter the amount you want to buy-in:')
        if ok:
            self.client_data[PC][self.client_index][PC_BuyInReq] = float(buy_in_amount)

######################################################################################################
# Dev stuff to make things faster:
######################################################################################################

    def setDevQuickLaunchSettings(self):
        self._win.line_user_name.setText('serverUser')
        self._win.line_game_name.setText('SERVER Game')
        self._win.line_starting_ammount.setText('10.0')
        self._win.line_currency.setText('RON')
        self._win.line_join_game_ip.setText(self._win.line_host_game_ip.text())
        self._win.line_join_game_port.setText(self._win.line_host_game_port.text())

