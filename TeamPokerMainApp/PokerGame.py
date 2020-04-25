from TeamPokerMainApp.GameUI.TeamPokerUIController import TeamPokerUIControllerClass
from TeamPokerMainApp.Multiplayer.NetworkPacket import NetworkPacketClass
from TeamPokerMainApp.Multiplayer.Server import MultiplayerServerClass
from TeamPokerMainApp.GameLogic.CardDeck import CardDeckClass
from TeamPokerMainApp.Multiplayer.Client import ClientClass
from TeamPokerMainApp.GameLogic.Dealer import DealerClass
from TeamPokerMainApp.Common.MethodDefinitions import *
from TeamPokerMainApp.Common.VariableDefinitions import *
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


class PokerGameClass:

    def __init__(self):
        self._win = TeamPokerUIControllerClass()
        self._packet = NetworkPacketClass()
        self.client_data = self._packet.get_network_packet_definition()
        self._deck = CardDeckClass()
        self.initConnectUiElements()
        self.initOtherStuff()
        self.setDevQuickLaunchSettings()

    def show_main_window(self):
        self._win.showMainWindow()

    def initConnectUiElements(self):
        self._win.connectStartHostingGameServer(self.start_poker_server)
        self._win.connectStartJoiningAGameServer(self.join_poker_server)
        self._win.connectButtonServerStartGame(lambda f: self.change_game_status_on_server(DEALER_thinks_GAME_is_PLAYING))
        self._win.connectButtonServerPauseGame(lambda f: self.change_game_status_on_server(DEALER_thinks_GAME_is_PAUSED))
        self._win.connectButtonServerEndGame(lambda f: self.change_game_status_on_server(DEALER_thinks_GAME_is_ENDING))
        self._win.connectActionSitOut(self.client_action_sit_out_or_playing)
        self._win.connectRaiseSliderMove(self.set_raise_button_text)

    def initOtherStuff(self):
        for player in range(MAX_CLIENTS):
            self._win.setUiHiddenPlayer(player, True)

################################################################################################
# 1. Network Stuff (Client & Server):
################################################################################################

    def start_poker_server(self):
        if self.check_if_all_host_server_fields_have_input():
            try:
                self._srv = MultiplayerServerClass(ip=self._win.getHostAGameIpAdress(), port=self._win.getHostAGamePortNumber())
            except Exception as e:
                print(f'ERROR: start_poker_server -> MultiplayerServerClass -> {e}')

            try:
                self.start_network_client(ip=self._win.getHostAGameIpAdress(), port=self._win.getHostAGamePortNumber())
            except Exception as e:
                print(f'ERROR: start_poker_server -> start_network_client -> {e}')

            self._win.goToPlayingArena()
            self._win.setServerControls(True)
        else:
            showCustomizedInfoWindow('Please fill all information!')

    def join_poker_server(self):
        if self.check_if_all_join_server_fields_have_input():
            try:
                self.start_network_client(ip=self._win.getJoinAGameIpAdress(), port=self._win.getJoinAGamePortNumber())
            except Exception as e:
                print(f'ERROR: join_poker_server -> start_network_client PLAYER -> {e}')
            self._win.goToPlayingArena()

    def start_network_client(self, ip, port):
        self._client = ClientClass(ip=ip, port=port)
        self.client_index = int(self._client.client_connect_to_server_and_get_position())
        self.table_spots = self.get_table_spots_from_client_index_point_of_view()
        self.client_init_game_data_from_own_ui()
        self.client_server_communication_loop()

    def client_server_communication_loop(self):
        self.communication_timer = QTimer(self._win)
        self.communication_timer.start(COMMUNCATION_TIME)
        self.communication_timer.timeout.connect(self.client_server_comm_action)

    def client_server_comm_action(self):
        try:
            # update the game_data with own ui info (mainly new actions, decisions by the player)
            self.client_update_game_data_from_own_ui()
            # Send your user update.
            # and get the update from all other clients, and dealer, centralized by the server.
            server_data = self._client.client_send_message_to_server_return_reply(self.client_data)
            # update our own UI based on the data received from the server (cards, other players, etc.)
            self.client_data = server_data
            self.client_update_own_ui_from_new_server_data()
        except Exception as e:
            print(f'client_server_comm_action -> {e}')

######################################################################################################
# 2. Client-Ui Logic:
######################################################################################################

    def client_init_game_data_from_own_ui(self):  # INIT stuff only!!!!!
        self.client_data["PlayerClient"][self.client_index]["TableSpot"] = self.client_index
        self.client_data["PlayerClient"][self.client_index]["Icon"] = self._win.getIconID()
        self.client_data["PlayerClient"][self.client_index]["Name"] = self._win.getUserName()

    def client_update_game_data_from_own_ui(self):
        # self.game_data["Player"][self.client_index]["TableSpot"] = self.client_index  # TODO: Allow player to change spot on table?
        if self._win.getActionPlayOrSitOut():  # if checked we are sitting out
            self.client_data["PlayerClient"][self.client_index]["GameStatus"] = PLAYER_STATUS_player_sit_out_next_turn
        else:
            self.client_data["PlayerClient"][self.client_index]["GameStatus"] = PLAYER_STATUS_player_is_playing
            # If we are playing also check if it's our turn to take a decision:
            if self.client_data["Dealer"]["NextDecision"] == self.client_index:
                playerAction = self._win.getPlayerAction()
                # if we decided copy the decision to the game_data
                if playerAction is not ACTION_UNDECIDED:
                    self.client_data["PlayerClient"][self.client_index]["GameAction"] = playerAction
            else:
                # if it's no longer our time to take a decision, reset the decision.
                self._win.reset_player_action_array()

    def client_update_own_ui_from_new_server_data(self):
        for player in range(MAX_CLIENTS):
            if self.client_data["PlayerServer"][player]["ConnectionStatus"] is not CONN_STATUS_EMPTY_SEAT:
                ui_pos = self.table_spots.index(player)
                self._win.setUiHiddenPlayer(pos=ui_pos, hidden=False)  # Show the player table in UI
                self._win.setUiPlayerName(ui_pos=ui_pos, name=self.client_data["PlayerClient"][player]["Name"])
                self._win.setUiPlayerIcons(ui_pos=ui_pos, icon_name=self.client_data["PlayerClient"][player]["Icon"])
                self.set_ui_player_dealer_icons(ui_pos=ui_pos, player=player)
                self.set_ui_player_money_and_currency(ui_pos=ui_pos, player=player)
                self.set_ui_player_status_text(ui_pos=ui_pos, player=player)
                self._win.setUiOtherPlayersCards(ui_pos)  # TODO: Show actual cards at end of round
            else:
                ui_pos = self.table_spots.index(player)
                self._win.setUiHiddenPlayer(pos=ui_pos, hidden=True)
        # update cards on table
        table_cards = self.client_data["Dealer"]["TableCards"]
        for card in range(NUMBER_OF_CARDS_ON_TABLE):
            card_name = self._deck.get_card_name_from_card_number(table_cards[card])
            self._win.setUiTableCard(card_number=card, card_name=card_name)
        # update cards in my hand
        player_cards = self.client_data["PlayerServer"][self.client_index]["PlayerCards"]  # returns array with card codes
        for card in range(NUMBER_OF_CARDS_IN_HAND):
            card_name = self._deck.get_card_name_from_card_number(player_cards[card])
            self._win.setUiEgoPlayerCards(card_number=card, card_name=card_name)
        # Update game status text.
        self._win.setGameStatusText(text=self.client_data["Dealer"]["GameStatus"])
        self._win.setNewPotValue(amount=self.client_data["Dealer"]["TablePot"], currency=self.client_data["Dealer"]["Currency"])
        self._win.setUiBurnedCards(number_of_burned_cards=self.client_data["Dealer"]["BurnedCards"])

    def client_action_sit_out_or_playing(self):
        # Checked = Sitting out
        # Unchecked = Playing
        if self._win.getActionPlayOrSitOut():
            self._win.togglePlayOrSitOutButtonText()
            self._win.setActionButtonsEnabled(False)
        else:
            self._win.togglePlayOrSitOutButtonText()
            self._win.setActionButtonsEnabled(True)

    def get_new_player_action(self):
        if self._win.getActionCall():
            self.client_data["PlayerClient"][self.client_index]["PlayerAction"] = ACTION_CALL
        elif self._win.getActionRaise():
            self.client_data["PlayerClient"][self.client_index]["PlayerAction"] = ACTION_RAISE
        elif self._win.getActionFold():
            self.client_data["PlayerClient"][self.client_index]["PlayerAction"] = ACTION_FOLD
        else:
            # If player didn't choose nothing automatically fold ?
            self.client_data["PlayerClient"][self.client_index]["PlayerAction"] = ACTION_FOLD

    def set_ui_player_status_text(self, ui_pos, player):
        gameAction = self.client_data["PlayerClient"][player]["PlayerAction"]
        betAmount = self.client_data["PlayerClient"][player]["BetAmount"]
        if self.client_data["PlayerClient"][player]["PlayerStatus"] is PLAYER_STATUS_player_sit_out_next_turn:
            self._win.setUiPlayerActions(ui_pos=ui_pos, status_text=f'Sitting Out!')
        elif self.client_data["Dealer"]["NextDecision"] == player:
            if gameAction == ACTION_CALL:
                self._win.setUiPlayerActions(ui_pos=ui_pos, status_text=f'Called {betAmount}')
            elif gameAction == ACTION_RAISE:
                self._win.setUiPlayerActions(ui_pos=ui_pos, status_text=f'Raised {betAmount}')
            elif gameAction == ACTION_FOLD:
                self._win.setUiPlayerActions(ui_pos=ui_pos, status_text=f'Fold!')
            else:
                self._win.setUiPlayerActions(ui_pos=ui_pos, status_text=f'Deciding...')

    def set_ui_player_dealer_icons(self, ui_pos, player):
        # There is only 1 dealer/blind icon spot. So if there are 2 players only and 1 is both dealer and big blind... fuck it.
        if self.client_data["PlayerServer"][player]["isDealer"] is TABLE_STATUS_is_DEALER:
            self._win.setUiDealerIcons(ui_pos=ui_pos, dealer_icon_name='dealer')
        elif self.client_data["PlayerServer"][player]["isBlind"] is TABLE_STATUS_is_SMALL_BLIND:
            self._win.setUiDealerIcons(ui_pos=ui_pos, dealer_icon_name='small_blind')
        elif self.client_data["PlayerServer"][player]["isBlind"] is TABLE_STATUS_is_BIG_BLIND:
            self._win.setUiDealerIcons(ui_pos=ui_pos, dealer_icon_name='big_blind')
        else:
            self._win.setUiDealerIcons(ui_pos=ui_pos, dealer_icon_name='')

    def set_ui_player_money_and_currency(self, ui_pos, player):
        moneyAvailable = self.client_data["PlayerServer"][player]["MoneyAvailable"]
        currency = self.client_data["Dealer"]["Currency"]
        self._win.setUiPlayerMoneyCurrency(ui_pos=ui_pos, amount=moneyAvailable, currency=currency)

    def set_minimum_maximum_slider_values(self):
        pass

    def set_raise_button_text(self):
        pass

    def change_game_status_on_server(self, status):
        # Normally only the server should start the game. This is a workaround.
        self.client_data["Dealer"]["GameStatus"] = status


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
        startingMoney = self._win.getStartingAmmount()
        currency = self._win.getCurrency()
        smallBlind = self._win.getSmallBlind()
        bigBlind = self._win.getBigBlind()
        blindInterval = self._win.getBlindInterval()
        tpl = (startingMoney, currency, smallBlind, bigBlind, blindInterval)
        return tpl

    def check_if_all_host_server_fields_have_input(self):
        rtrn = False
        if self._win.getStartingAmmount() > 0 and len(self._win.getCurrency()) > 0 and self._win.getSmallBlind() > 0 and self._win.getBigBlind() > 0:
            rtrn = True
        return rtrn

    def check_if_all_join_server_fields_have_input(self):
        rtrn = False
        if self._win.getStartingAmmount() > 0 and len(self._win.getCurrency()) > 0 and self._win.getSmallBlind() > 0 and self._win.getBigBlind() > 0:
            rtrn = True
        return rtrn

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

