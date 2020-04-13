from TeamPokerMainApp.PokerGame.GameUI.TeamPokerUIController import TeamPokerUIControllerClass
from TeamPokerMainApp.PokerGame.Multiplayer.NetworkPacket import NetworkPacketClass
from TeamPokerMainApp.PokerGame.Multiplayer.Server import MultiplayerServerClass
from TeamPokerMainApp.PokerGame.Multiplayer.Client import ClientClass
from TeamPokerMainApp.PokerGame.GameLogic.Dealer import DealerClass
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
        self.game_status = GAME_STATUS_WAITING_FOR_PLAYERS
        self._win = TeamPokerUIControllerClass()
        self._packet = NetworkPacketClass()
        self.game_data = self._packet.get_game_data()
        self.initConnectButtons()
        self.setDevQuickLaunchSettings()

    def show_main_window(self):
        self._win.showMainWindow()

    def initConnectButtons(self):
        self._win.connectStartHostingGameServer(self.start_poker_server)
        self._win.connectStartJoiningAGameServer(self.join_poker_server)
        self._win.connectButtonDevStartDealer(self.force_new_round)

################################################################################################
# 1. Network Stuff (Client & Server):
#   Shall set up rules for the game. Small/Big Blind, Buy-In Rules, etc.
#   Starts the Multiplayer Server which accepts incoming connections.
#   Starts Host Client (which acts as a dealer also).
#   Dealer does all game logic calculations based on information received from the players.
################################################################################################

    def start_poker_server(self):
        if self.check_if_all_host_server_fields_have_input():
            self._win.setWindowTitle(self._win.getGameName())
            try:
                self._srv = MultiplayerServerClass(ip=self._win.getHostAGameIpAdress(), port=self._win.getHostAGamePortNumber())
            except Exception as e:
                print(f'ERROR: start_poker_server MultiplayerServerClass -> {e}')
            try:
                self._dealer = DealerClass(self.get_game_rules(), self._packet.get_game_data())
            except Exception as e:
                print(f'ERROR: start_poker_server DealerClass -> {e}')
            try:
                self.start_network_client(ip=self._win.getHostAGameIpAdress(), port=self._win.getHostAGamePortNumber())
            except Exception as e:
                print(f'ERROR: start_poker_server -> start_network_client as DEALER -> {e}')
            self._win.goToPlayingArena()
            self.update_self_ui()
        else:
            showCustomizedInfoWindow('Please fill all information!')

    def join_poker_server(self):
        if self.check_if_all_join_server_fields_have_input():
            try:
                self.start_network_client(ip=self._win.getJoinAGameIpAdress(), port=self._win.getJoinAGamePortNumber())
            except Exception as e:
                print(f'ERROR: start_network_client -> start_network_client PLAYER -> {e}')
            self._win.goToPlayingArena()

    def start_network_client(self, ip, port):
        self._client = ClientClass(ip=ip, port=port)
        self.client_index = int(self._client.connect_to_server_and_get_position())

        self.game_data["PlayersInfo"][self.client_index][PINFO_tableSpot] = self.client_index  # each player puts his own index
        self.game_data["PlayersInfo"][self.client_index][PINFO_icon] = self._win.getIconID()
        self.game_data["PlayersInfo"][self.client_index][PINFO_name] = self._win.getUserName()
        self.game_data["PlayersInfo"][self.client_index][PINFO_status] = STATUS_PLAYING
        self.client_server_communication_loop()

    def client_server_communication_loop(self):
        self.dealer_update_timer = QTimer(self._win)
        self.dealer_update_timer.start(300)
        self.dealer_update_timer.timeout.connect(self.client_server_comm_action)

    def client_server_comm_action(self):
        # update the game_data with own ui info (mainly new actions, decisions by the player)
        self.client_update_game_data_from_own_ui()

        # Send your user update.
        # and get the update from all other clients, and dealer, centralized by the server.
        server_data = self._client.client_communicate_with_server(self.game_data)

        # update our own UI based on the data received from the server (cards, other players, etc.)
        try:
            self.client_update_game_data_from_server_data(server_data)
            self.client_update_ui()
        except Exception as e:
            print(f'client_server_comm_action -> client_update_data_and_ui_based_on_server_update -> {e}')

        if self.client_index == DEALER:
            try:
                # copy the player info
                self.game_data["PlayersInfo"] = server_data["PlayersInfo"]
                self.dealer_evaluate_next_game_step()
            except Exception as e:
                print(f'client_server_comm_action -> dealer stuff failed -> {e}')

######################################################################################################
# 3. Dealer Logic:
######################################################################################################

    def dealer_evaluate_next_game_step(self):
        # if self.count_number_of_playing_players() > 1 and self.game_status is GAME_STATUS_NEW_ROUND_READY:
        if self.game_status is GAME_STATUS_NEW_ROUND_READY:
            self.game_status = GAME_STATUS_PLAYER_DECIDING
            self._dealer.new_poker_round()

######################################################################################################
# 4. Client Logic:
######################################################################################################

    def client_update_game_data_from_own_ui(self):
        self.game_data["PlayersInfo"][self.client_index][PINFO_tableSpot] = self.client_index
        self.game_data["PlayersInfo"][self.client_index][PINFO_name] = self._win.getUserName()
        self.game_data["PlayersInfo"][self.client_index][PINFO_icon] = self._win.getIconID()
        self.game_data["PlayersInfo"][self.client_index][PINFO_actionID] = ACTION_CALL
        self.game_data["PlayersInfo"][self.client_index][PINFO_status] = STATUS_PLAYING

    def client_update_game_data_from_server_data(self, server_data):
        self.game_data["Dealer"] = server_data["Dealer"]
        self.game_data["PlayersGame"] = server_data["PlayersGame"]
        # update the PlayersInfo for every other player.
        for player in range(MAX_CLIENTS):
            if player != self.client_index:
                self.game_data["PlayersInfo"][player] = server_data["PlayersInfo"][player]

    def client_update_ui(self):
        for player in range(MAX_CLIENTS):
            ui_pos = 1  # TODO: Fix table positioning to show corectly on all clients... maybe using ["PlayersInfo"][client_index][PINFO_tableSpot]
            if self.game_data["PlayersInfo"][player][PINFO_status] is not STATUS_EMPTY_SEAT and player != self.client_index:
                self._win.setUiPlayerName(ui_pos=ui_pos, name=self.game_data["PlayersInfo"][player][PINFO_name])
                self._win.setUiPlayerIcons(ui_pos=ui_pos, icon_name=self.game_data["PlayersInfo"][player][PINFO_icon])
                self._win.setUiPlayerMoneyCurrency(ui_pos=ui_pos, ammount=self.game_data["PlayersGame"][player][PGAME_moneyAvailable])
                self._win.setUiDealerIcons(ui_pos=ui_pos, dealer_icon_name=self.game_data["PlayersGame"][player][PGAME_dealerIcon])
                self._win.setUiPlayerActions(ui_pos=ui_pos, action=self.game_data["PlayersInfo"][player][PINFO_actionID])
                self._win.setUiOtherPlayersCards(ui_pos)  #TODO: Show actual cards at end of round
                ui_pos += 1
        # update cards on table
        table_cards = self.game_data["Dealer"]["TableCards"]
        for card in range(NUMBER_OF_CARDS_ON_TABLE):
            self._win.setUiTableCard(card_number=card, card_code=table_cards[card])
        # update cards in hand
        player_cards = self.game_data["PlayersGame"][self.client_index][PGAME_playerCards]  # returns array with card codes
        for card in range(NUMBER_OF_CARDS_IN_HAND):
            self._win.setUiEgoPlayerCards(card_number=card, card_code=player_cards[card])

######################################################################################################
# 5. Other Logic:
######################################################################################################

    def update_self_ui(self):
        self._win.setUiPlayerIcons(ui_pos=self.client_index, icon_name=self._win.getIconID())
        self._win.setUiPlayerMoneyCurrency(ui_pos=self.client_index, ammount=self.game_data["PlayersGame"][self.client_index][PGAME_moneyAvailable])
        self._win.setUiPlayerName(ui_pos=self.client_index, name=self.game_data["PlayersInfo"][self.client_index][PINFO_name])

    def get_game_rules(self):
        startingMoney = self._win.getStartingAmmount()
        currency = self._win.getCurrency()
        smallBlind = self._win.getSmallBlind()
        bigBlind = self._win.getBigBlind()
        blindInterval = self._win.getBlindInterval()
        tpl = (startingMoney, currency, smallBlind, bigBlind, blindInterval)
        print(tpl)
        return tpl

    def check_if_all_host_server_fields_have_input(self):
        rtrn = False
        print(self._win.getStartingAmmount())
        if self._win.getStartingAmmount() > 0 and len(self._win.getCurrency()) > 0 and self._win.getSmallBlind() > 0 and self._win.getBigBlind() > 0:
            rtrn = True
        return rtrn

    def check_if_all_join_server_fields_have_input(self):
        rtrn = False
        print(self._win.getStartingAmmount())
        if self._win.getStartingAmmount() > 0 and len(self._win.getCurrency()) > 0 and self._win.getSmallBlind() > 0 and self._win.getBigBlind() > 0:
            rtrn = True
        return rtrn

    def count_number_of_playing_players(self):
        playingPlayers = 0
        for player in range(1, MAX_CLIENTS):
            if self.game_data["PlayersInfo"][player][PINFO_status] is STATUS_PLAYING:
                playingPlayers += 1
        return playingPlayers

######################################################################################################
# 3. Dev stuff to make things faster:
######################################################################################################

    def setDevQuickLaunchSettings(self):
        self._win.line_user_name.setText('testUserName')
        self._win.line_game_name.setText('SERVER Game')
        self._win.line_starting_ammount.setText('10.0')
        self._win.line_currency.setText('EUR')
        self._win.line_join_game_ip.setText(self._win.line_host_game_ip.text())
        self._win.line_join_game_port.setText(self._win.line_host_game_port.text())

    def force_new_round(self):
        self.game_status = GAME_STATUS_NEW_ROUND_READY
        print(f'DEV: Force new round! game_status = {self.game_status}')
