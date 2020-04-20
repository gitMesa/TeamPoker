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
# 1. Mode Server:
#   Shall set up rules for the game. Small/Big Blind, Buy-In Rules, etc.
#   Shall create a 'Dealer' client, and a 'User' Client.
#   Shall accept connections from other Clients.
#   'Dealer Client' shall handle the table/dealer/pot/logic.
#   Shall send cards to Players(other Clients).
#   Shall receive actions from Players(other Clients).
#
# 2. Client Mode:
#   Shall connect to the server providing UserName and UserIcon?
#   Shall receive from Server cards.
#   Shall send to Server Actions.
#
###################################################################


class PokerGameClass:

    def __init__(self):
        self._win = TeamPokerUIControllerClass()
        self._packet = NetworkPacketClass()
        self._deck = CardDeckClass()
        self.game_data = self._packet.get_game_data()
        self.game_status = DEALER_thinks_GAME_is_PAUSED
        self.initConnectUiElements()
        self.initOtherStuff()
        self.setDevQuickLaunchSettings()

    def show_main_window(self):
        self._win.showMainWindow()

    def initConnectUiElements(self):
        self._win.connectStartHostingGameServer(self.start_poker_server)
        self._win.connectStartJoiningAGameServer(self.join_poker_server)
        self._win.connectButtonServerStartGame(self.dealer_start_game)
        self._win.connectButtonServerPauseGame(lambda f: self._dealer.set_dealer_status(DEALER_thinks_GAME_is_PAUSED))
        self._win.connectButtonServerEndGame(lambda f: self._dealer.set_dealer_status(DEALER_thinks_GAME_is_ENDING))
        self._win.connectActionSitOut(self.set_action_sit_out_or_playing)
        self._win.connectRaiseSliderMove(self.set_raise_button_text)

    def initOtherStuff(self):
        for player in range(MAX_CLIENTS):
            self._win.setUiHiddenPlayer(player, True)

################################################################################################
# 1. Network Stuff (Client & Server):
#   Shall set up rules for the game. Small/Big Blind, Buy-In Rules, etc.
#   Starts the Multiplayer Server which accepts incoming connections.
#   Starts Host Client (which acts as a dealer also).
#   Dealer does all game logic calculations based on information received from the players.
################################################################################################

    def start_poker_server(self):
        if self.check_if_all_host_server_fields_have_input():
            try:
                self._srv = MultiplayerServerClass(ip=self._win.getHostAGameIpAdress(), port=self._win.getHostAGamePortNumber())
            except Exception as e:
                print(f'ERROR: start_poker_server MultiplayerServerClass -> {e}')

            try:
                self._dealer = DealerClass(self.get_game_rules(), self._deck)
                self.dealer_set_game_rules_to_network_packet()
            except Exception as e:
                print(f'ERROR: start_poker_server DealerClass -> {e}')

            try:
                self.start_network_client(ip=self._win.getHostAGameIpAdress(), port=self._win.getHostAGamePortNumber())
            except Exception as e:
                print(f'ERROR: start_poker_server -> start_network_client as DEALER -> {e}')

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
        # update the game_data with own ui info (mainly new actions, decisions by the player)
        self.client_update_game_data_from_own_ui()
        # Send your user update.
        # and get the update from all other clients, and dealer, centralized by the server.
        server_data = self._client.client_send_message_to_server_return_reply(self.game_data)
        # update our own UI based on the data received from the server (cards, other players, etc.)
        try:
            # Update local data with server data.
            self.game_data = server_data
            self.client_update_own_ui_from_new_server_data()
        except Exception as e:
            print(f'client_server_comm_action -> client_update_own_ui_from_new_server_data -> {e}')
        if self.client_index == DEALER:
            try:
                # copy the player info
                self.game_data["Player"] = server_data["Player"]
                # send the data to the Dealer Class
                self._dealer.set_data_to_dealer_game_data(self.game_data)
                # call dealer class to do its magic
                self.dealer_evaluate_next_game_step()
                # get data back after analysis by dealer class
                self.game_data = self._dealer.get_dealer_game_data()
            except Exception as e:
                print(f'client_server_comm_action -> dealer_evaluate_next_game_step -> {e}')

######################################################################################################
# 3. Dealer Logic:
######################################################################################################

    def dealer_evaluate_next_game_step(self):
        self._dealer.set_dealer_status(DEALER_thinks_GAME_is_PLAYING)
        if not self.are_enough_players_playing():
            self._dealer.set_dealer_status(DEALER_thinks_GAME_is_PAUSED)
        self._dealer.dealer_evaluate_next_step()          # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< THIS IS WHAT YOU ARE LOOKING FOR

    def are_enough_players_playing(self):
        number = 0
        for player in range(MAX_CLIENTS):
            if self.game_data["Player"][player]["GameStatus"] is GAME_STATUS_PLAYER_PLAYING:
                number += 1
        return number >= 2

    def dealer_set_game_rules_to_network_packet(self):
        self.game_data["Dealer"]["GameName"] = self._win.getGameName()
        self.game_data["Dealer"]["Currency"] = self.get_game_rules()[1]
        self.game_data["Dealer"]["BigBlind"] = self.get_game_rules()[3]

    def dealer_start_game(self):
        self._dealer.dealer_start_the_game()

######################################################################################################
# 4. Client Logic:
######################################################################################################

    def client_init_game_data_from_own_ui(self):  # INIT stuff only!!!!!
        self.game_data["Player"][self.client_index]["TableSpot"] = self.client_index
        self.game_data["Player"][self.client_index]["Icon"] = self._win.getIconID()
        self.game_data["Player"][self.client_index]["Name"] = self._win.getUserName()

    def client_update_game_data_from_own_ui(self):
        # self.game_data["Player"][self.client_index]["TableSpot"] = self.client_index  # TODO: Allow player to change spot on table?
        self.game_data["Player"][self.client_index]["ConnectionStatus"] = CONN_STATUS_CONNECTED
        self.game_data["Player"][self.client_index]["GameAction"] = self._win.getPlayerAction()
        if self._win.getActionPlayOrSitOut():  # if checked we are sitting out
            self.game_data["Player"][self.client_index]["GameStatus"] = GAME_STATUS_PLAYER_SIT_OUT_TURN
        else:
            self.game_data["Player"][self.client_index]["GameStatus"] = GAME_STATUS_PLAYER_PLAYING

    def client_update_own_ui_from_new_server_data(self):
        for player in range(MAX_CLIENTS):
            if self.game_data["Player"][player]["ConnectionStatus"] is not CONN_STATUS_EMPTY_SEAT:
                ui_pos = self.table_spots.index(player)
                self._win.setUiHiddenPlayer(pos=ui_pos, hidden=False)  # Show the player table in UI
                self._win.setUiPlayerName(ui_pos=ui_pos, name=self.game_data["Player"][player]["Name"])
                self._win.setUiPlayerIcons(ui_pos=ui_pos, icon_name=self.game_data["Player"][player]["Icon"])
                self._win.setUiDealerIcons(ui_pos=ui_pos, dealer_icon_name=self.game_data["Player"][player]["DealerIcon"])
                self.set_ui_player_money_and_currency(ui_pos=ui_pos, player=player)
                self.set_ui_player_status_text(ui_pos=ui_pos, player=player)
                self._win.setUiOtherPlayersCards(ui_pos)  # TODO: Show actual cards at end of round
            else:
                ui_pos = self.table_spots.index(player)
                self._win.setUiHiddenPlayer(pos=ui_pos, hidden=True)
        # update cards on table
        table_cards = self.game_data["Dealer"]["TableCards"]
        for card in range(NUMBER_OF_CARDS_ON_TABLE):
            card_name = self._deck.get_card_name_from_card_number(table_cards[card])
            self._win.setUiTableCard(card_number=card, card_name=card_name)
        # update cards in my hand
        player_cards = self.game_data["Player"][self.client_index]["PlayerCards"]  # returns array with card codes
        for card in range(NUMBER_OF_CARDS_IN_HAND):
            card_name = self._deck.get_card_name_from_card_number(player_cards[card])
            self._win.setUiEgoPlayerCards(card_number=card, card_name=card_name)
        # Update game status text.
        self._win.setGameStatusText(text=self.game_data["Dealer"]["GameStatus"])
        self._win.setNewPotValue(amount=self.game_data["Dealer"]["TablePot"], currency=self.game_data["Dealer"]["Currency"])
        self._win.setUiBurnedCards(number_of_burned_cards=self.game_data["Dealer"]["BurnedCards"])

    def set_action_sit_out_or_playing(self):
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
            self.game_data["Player"][self.client_index]["GameAction"] = ACTION_CALL
        elif self._win.getActionRaise():
            self.game_data["Player"][self.client_index]["GameAction"] = ACTION_RAISE
        elif self._win.getActionFold():
            self.game_data["Player"][self.client_index]["GameAction"] = ACTION_FOLD
        else:
            # If player didn't choose nothing automatically fold ?
            self.game_data["Player"][self.client_index]["GameAction"] = ACTION_FOLD

    def set_ui_player_status_text(self, ui_pos, player):
        gameAction = self.game_data["Player"][player]["GameAction"]
        betAmount = self.game_data["Player"][player]["BetAmount"]
        if self.game_data["Player"][player]["GameStatus"] is GAME_STATUS_PLAYER_SIT_OUT_TURN:
            self._win.setUiPlayerActions(ui_pos=ui_pos, status_text=f'Sitting Out!')
        elif gameAction == ACTION_CALL:
            self._win.setUiPlayerActions(ui_pos=ui_pos, status_text=f'Called {betAmount}')
        elif gameAction == ACTION_RAISE:
            self._win.setUiPlayerActions(ui_pos=ui_pos, status_text=f'Raised {betAmount}')
        elif gameAction == ACTION_FOLD:
            self._win.setUiPlayerActions(ui_pos=ui_pos, status_text=f'Fold!')
        else:
            self._win.setUiPlayerActions(ui_pos=ui_pos, status_text=f'Deciding...')

    def set_ui_player_money_and_currency(self, ui_pos, player):
        moneyAvailable = self.game_data["Player"][player]["MoneyAvailable"]
        currency = self.game_data["Dealer"]["Currency"]
        self._win.setUiPlayerMoneyCurrency(ui_pos=ui_pos, amount=moneyAvailable, currency=currency)

    def set_minimum_maximum_slider_values(self):
        pass

    def set_raise_button_text(self):
        pass

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
        self._win.line_user_name.setText('testUserName')
        self._win.line_game_name.setText('SERVER Game')
        self._win.line_starting_ammount.setText('10.0')
        self._win.line_currency.setText('RON')
        self._win.line_join_game_ip.setText(self._win.line_host_game_ip.text())
        self._win.line_join_game_port.setText(self._win.line_host_game_port.text())

