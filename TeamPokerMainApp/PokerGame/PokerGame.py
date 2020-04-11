from TeamPokerMainApp.PokerGame.GameUI.UiCode.TeamPokerUIController import TeamPokerUIControllerClass
from TeamPokerMainApp.PokerGame.Multiplayer.Server import MultiplayerServerClass
from TeamPokerMainApp.PokerGame.Multiplayer.Client import ClientClass
from TeamPokerMainApp.PokerGame.GameLogic.Dealer import DealerClass
from TeamPokerMainApp.Common.MethodDefinitions import *
from TeamPokerMainApp.Common.VariableDefinitions import *
from PyQt5.Qt import QTimer
import time

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
        self.initConnectButtons()
        self.setDevQuickLaunchSettings()

    def show_main_window(self):
        self._win.showMainWindow()

    def initConnectButtons(self):
        self._win.connectButtonHostGame(self.start_poker_server)
        self._win.connectButtonJoinGame(lambda sc: self.start_poker_client(ip=self._win.getJoinAGameIpAdress(), port=self._win.getJoinAGamePortNumber()))
        self._win.connectButtonDevStartDealer(self.dealer_evaluate_next_game_step)

###################################################################
# 1. Mode Server:
#   Shall accept connections from Clients.
#   Shall receive actions from Players(Client Mode).
#   Shall set up rules for the game. Small/Big Blind, Buy-In Rules, etc.
#   Shall remember the Buy-In / Money of Players and show them in a statistics tab.
#   Shall handle the table/dealer/pot/logic.
#   Shall send cards to Players(Client Mode).
###################################################################

    def start_poker_server(self):
        if self.check_if_all_fields_have_input():
            self._win.setWindowTitle(self._win.getGameName())
            try:
                self._srv = MultiplayerServerClass(ip=self._win.getHostAGameIpAdress(), port=self._win.getHostAGamePortNumber())
            except Exception as e:
                print(f'ERROR: start_poker_server _srv -> {e}')
            try:
                self._dealer = DealerClass(self.get_game_rules())
            except Exception as e:
                print(f'ERROR: start_poker_server _dealer -> {e}')
            try:
                self.start_network_client(ip=self._win.getHostAGameIpAdress(), port=self._win.getHostAGamePortNumber(), type=DEALER)
            except Exception as e:
                print(f'ERROR: start_poker_server -> start_network_client DEALER -> {e}')
            try:
                self.start_network_client(ip=self._win.getHostAGameIpAdress(), port=self._win.getHostAGamePortNumber(), type=PLAYER)
            except Exception as e:
                print(f'ERROR: start_poker_server -> start_network_client PLAYER -> {e}')
            self._win.goToPlayingArena()
        else:
            showCustomizedInfoWindow('Please fill all information!')

    def check_if_all_fields_have_input(self):
        rtrn = False
        print(self._win.getStartingAmmount())
        if self._win.getStartingAmmount() > 0 and len(self._win.getCurrency()) > 0 and self._win.getSmallBlind() > 0 and self._win.getBigBlind() > 0:
            rtrn = True
        return rtrn

    def get_game_rules(self):
        starting_ammount = self._win.getStartingAmmount()
        currency = self._win.getCurrency()
        small_blind = self._win.getSmallBlind()
        big_blind = self._win.getBigBlind()
        blind_interval = self._win.getBlindInterval()
        tpl = (starting_ammount, currency, small_blind, big_blind, blind_interval)
        print(tpl)
        return tpl

    def start_network_client(self, ip, port, type):
        if type == DEALER:
            self._dealerClient = ClientClass(ip=ip, port=port)
            dealer_position = self._dealerClient.connect_to_server_and_get_player_position()
            if int(dealer_position) == DEALER:
                self.dealer_server_communication_loop()
                # self.send_dealer_update_to_server()
            else:
                showCustomizedErrorWindow(f'start_network_client -> Something went wrong with dealer position being {DEALER}')
        elif type == PLAYER:
            self._client = ClientClass(ip=ip, port=port)
            self.position_at_table = int(self._client.connect_to_server_and_get_player_position())
            if self.position_at_table > 0:
                # update game info with your information
                while True:
                    game_data = self._dealer.get_thread_safe_comm_packet()
                    if game_data is not GAME_DATA_IN_USE:
                        game_data["Players"][self.position_at_table][PACKET_icon] = self._win.getIconID()
                        game_data["Players"][self.position_at_table][PACKET_name] = self._win.getUserName()
                        self._dealer.unlock_thread_safe_comm_packet()
                        self.client_server_communication_loop()
                        break

    def dealer_server_communication_loop(self):
        self.dealer_update_timer = QTimer(self._win)
        self.dealer_update_timer.start(300)
        self.dealer_update_timer.timeout.connect(self.send_dealer_update_to_server)

    def client_server_communication_loop(self):
        self.client_update_timer = QTimer(self._win)
        self.client_update_timer.start(500)
        self.client_update_timer.timeout.connect(self.send_client_update_to_server)

    def send_dealer_update_to_server(self):
        # self.dealer_evaluate_next_game_step()
        while True:
            game_data = self._dealer.get_thread_safe_comm_packet()
            if game_data is not GAME_DATA_IN_USE:  # if GAME_DATA_PACKET is successfully locked from other thread access
                print(f'DEALER: Dealer sent update to server.')
                self._client.send_dealer_update_to_server(game_data)
                self._dealer.unlock_thread_safe_comm_packet()
                break

    def send_client_update_to_server(self):
        while True:
            game_data = self._dealer.get_thread_safe_comm_packet()
            if game_data is not GAME_DATA_IN_USE:  # if GAME_DATA_PACKET is successfully locked from other thread access
                # first update the game_data from our own UI actions, settings, etc.
                self.update_game_data_from_own_ui(game_data)
                # send the game_data to the dealer, and receive his update
                dealer_data = self._client.send_client_data_and_receive_dealer_data(game_data)
                # unlock game data for use
                print(f'C{self.position_at_table} sent update to server, received dealer data.')
                self._dealer.unlock_thread_safe_comm_packet()
                # update our own UI based on the data received from the dealer (cards, other players, etc.)
                self.update_client_ui_based_on_server_update(dealer_data)
                break


    def dealer_evaluate_next_game_step(self):
        if self.count_number_of_playing_players() > 1 and self.game_status is GAME_STATUS_NEW_ROUND_READY:
            self._dealer.new_poker_round()

    def count_number_of_playing_players(self):
        playingPlayers = 0
        for player in range(1, MAX_CLIENTS):
            # if self._dealer.get_thread_safe_comm_packet()["Players"][player][PACKET_status] is STATUS_PLAYING:
                playingPlayers += 1
        return playingPlayers

######################################################################################################
# 2. Client Mode:
#   Shall connect to the server.
#   Shall update the packet based on own information (actions, bets, etc).
#   Shall contact the server asking for updates from UI from other players.
######################################################################################################


    def update_client_ui_based_on_server_update(self, game_data):
        # update cards only for current client
        player_cards = game_data["Players"][self.position_at_table][PACKET_player_cards]
        for card_number in player_cards:
            self._win.setEgoPlayerCards(card_number=card_number, card_code=player_cards[card_number])
        # update UI information for all other clients
        for player in range(1, MAX_CLIENTS):
            player_status = game_data["Players"][player][PACKET_status]
            if player_status is not STATUS_EMPTY_SEAT:
                # money each player has available
                playerMoney = game_data["Players"][player][PACKET_money_available]
                self._win.setUiPlayerMoneyCurrency(player=player, ammount=playerMoney)
                # dealer / small blind / big blind icon
                dealer_icon_name = game_data["Players"][player][PACKET_dealer_icon]
                self._win.setUiDealerIcons(player=player, dealer_icon_name=dealer_icon_name)
                # action that the player took
                player_action = game_data["Players"][player]

    def update_game_data_from_own_ui(self, game_data):
        # game_data["Players"][self.position_at_table][PACKET_action_id] = None # user action from GUI
        # self.set_thread_safe_comm_packet(game_data)
        pass


######################################################################################################
# 3. Dev stuff to make things faster:
######################################################################################################

    def setDevQuickLaunchSettings(self):
        self._win.line_user_name.setText('testUserName')
        self._win.line_game_name.setText('testGameName')
        self._win.line_starting_ammount.setText('10.0')
        self._win.line_currency.setText('EUR')
