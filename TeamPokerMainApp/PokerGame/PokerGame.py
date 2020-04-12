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
        self.game_status = GAME_STATUS_NEW_ROUND_READY
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
        self._win.connectButtonDevStartDealer(self.dealer_evaluate_next_game_step)

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

        if self.client_index == DEALER:
            self.dealer_server_communication_loop()
        elif self.client_index > DEALER:
            self.client_server_communication_loop()

    def dealer_server_communication_loop(self):
        self.dealer_update_timer = QTimer(self._win)
        self.dealer_update_timer.start(500)
        self.dealer_update_timer.timeout.connect(self.dealer_server_comm_action)

    def client_server_communication_loop(self):
        self.client_update_timer = QTimer(self._win)
        self.client_update_timer.start(900)
        self.client_update_timer.timeout.connect(self.client_server_comm_action)

    def dealer_server_comm_action(self):
        if self._srv.conn_player_number >= 2:
            try:
                client_data = self._client.get_reply_from_server()
                print(f'DEALER received Client{client_data["Sender"]} data. ')
                self.dealer_evaluate_user_data(data=client_data)
                self.dealer_evaluate_next_game_step()
                self.game_data["Sender"] = DEALER
                self._client.send_message_to_server(self.game_data)
            except Exception as e:
                print(f'dealer_server_comm_action -> {e}')

    def client_server_comm_action(self):
        self.game_data["Sender"] = self.client_index
        # first update the game_data from our own UI actions, settings, etc.
        self.client_update_game_data_from_own_ui()
        # send the game_data to the dealer, and receive his update
        try:
            self._client.send_message_to_server(self.game_data)
            dealer_data = self._client.get_reply_from_server()
            print(f'C{self.client_index} sent update to server, received dealer C{dealer_data["Sender"]} data.')
            # update our own UI based on the data received from the dealer (cards, other players, etc.)
            self.client_update_data_and_ui_based_on_dealer_update(dealer_data)
        except Exception as e:
            print(f'send_client_update_to_server -> {e}')

######################################################################################################
# 2. Other Server-Client Logic:
######################################################################################################


######################################################################################################
# 3. Dealer Logic:
######################################################################################################

    def dealer_evaluate_user_data(self, data):
        sender = self.game_data["Sender"]
        self.game_data["PlayersInfo"][sender] = data["PlayersInfo"][sender]

    def dealer_evaluate_next_game_step(self):
        if self.count_number_of_playing_players() > 1 and self.game_status is GAME_STATUS_NEW_ROUND_READY:
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

    def client_update_data_and_ui_based_on_dealer_update(self, dealer_data):
        if dealer_data["Sender"] == DEALER:
            self.game_data["Dealer"] = dealer_data["Dealer"]
            self.game_data["PlayersGame"] = dealer_data["PlayersGame"]

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
