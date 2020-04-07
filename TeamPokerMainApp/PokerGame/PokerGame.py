from TeamPokerMainApp.PokerGame.GameUI.UiCode.TeamPokerUIController import TeamPokerUIControllerClass
from TeamPokerMainApp.PokerGame.Multiplayer.NetworkPacket import NetworkPacketClass
from TeamPokerMainApp.PokerGame.Multiplayer.Server import MultiplayerServerClass
from TeamPokerMainApp.PokerGame.Multiplayer.Client import ClientClass
from TeamPokerMainApp.PokerGame.GameLogic.Dealer import DealerClass
from TeamPokerMainApp.Common.MethodDefinitions import *
from PyQt5.Qt import QTimer
from TeamPokerMainApp.Common.VariableDefinitions import *

####################################################################
# Purpose of this class is to connect the UI to the Game Logic part.
# From the UI you can either create a Server or a Client
#
# 1. Mode Server:
#   Shall set up rules for the game. Small/Big Blind, Buy-In Rules, etc.
#   Shall accept connections from Clients.
#   Shall remember the Buy-In / Money of Players and show them in a statistics tab.
#   Shall handle the table/dealer/pot/logic.
#   Shall send cards to Players(Client Mode).
#   Shall receive actions from Players(Client Mode).
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
        self._comm = NetworkPacketClass()
        self.initConnectButtons()

    def show_main_window(self):
        self._win.showMainWindow()

    def initConnectButtons(self):
        self._win.connectButtonHostGame(self.start_poker_server)
        self._win.connectButtonJoinGame(self.start_poker_client)
        self._win.connectButtonDevStartDealer(self.dealer_start_round)

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
                self._srv = MultiplayerServerClass(ip=self._win.getHostAGameIpAdress(), port=self._win.getHostAGamePortNumber(), packet=self._comm.getCommunicationPacket())
            except Exception as e:
                print(f'ERROR: start_poker_server srv: {e}')
            try:
                self._dealer = DealerClass(self.get_game_rules(), self._comm.getCommunicationPacket())
            except Exception as e:
                print(f'ERROR: start_poker_server dealer: {e}')
            try:
                self.start_dealer_client()
                self.start_poker_client()
            except Exception as e:
                print(f'ERROR: start_poker_server client: {e}')

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

    def start_dealer_client(self):
        self._client = ClientClass(ip=self._win.getJoinAGameIpAdress(), port=self._win.getJoinAGamePortNumber())
        dealer_position = self._client.connect_to_server_and_get_player_position()
        if dealer_position is 0:
            self.dealer_server_loop()
        else:
            showCustomizedErrorWindow('Something went wrong with dealer position being 0')

    def dealer_server_loop(self):
        self.dealer_update_timer = QTimer(self._win)
        self.dealer_update_timer.start(95)
        self.dealer_update_timer.timeout.connect(self.send_dealer_update_to_server)

    def send_dealer_update_to_server(self):
        self.dealer_evaluate_next_game_step()
        self._client.send_dealer_update_to_server(self._comm.getCommunicationPacket())

    def dealer_evaluate_next_game_step(self):
        if self.count_number_of_playing_players() > 1 and self.game_status is GAME_STATUS_NEW_ROUND_READY:
            self._dealer.new_poker_round()

    def count_number_of_playing_players(self):
        playingPlayers = 0
        for player in range(1, NO_OF_CLIENTS):
            if self._comm.getCommunicationPacket()["Players"][player][COMM_PACKET_status] is STATUS_PLAYING:
                playingPlayers += 1
        return playingPlayers


######################################################################################################
# 2. Client Mode:
#   Shall connect to the server.
#   Shall update the packet based on own information (actions, bets, etc).
#   Shall contact the server asking for updates from UI from other players.
######################################################################################################

    def start_poker_client(self):
        self._client = ClientClass(ip=self._win.getJoinAGameIpAdress(), port=self._win.getJoinAGamePortNumber())
        self.position_at_table = self._client.connect_to_server_and_get_player_position()
        self.request_update_from_server_loop()

    def request_update_from_server_loop(self):
        self.client_update_timer = QTimer(self._win)
        self.client_update_timer.start(200)
        self.client_update_timer.timeout.connect(self.request_update)

    def request_update(self):
        #TODO: update my own packet info based on the UI settings before sending it to the server
        update_from_server = self._client.send_and_receive_update(self._comm.getCommunicationPacket())
        self.update_client_ui_based_on_server_update(update_from_server)

    def update_client_ui_based_on_server_update(self, packet_received_from_server):
        # update cards only for current client
        player_cards = packet_received_from_server["Players"][self.position_at_table][COMM_PACKET_player_cards]
        for card_number in player_cards:
            self._win.setEgoPlayerCards(card_number=card_number, card_code=player_cards[card_number])
        # update UI information for all other clients
        for player in range(1, NO_OF_CLIENTS):
            player_status = packet_received_from_server["Players"][player][COMM_PACKET_status]
            if player_status is not STATUS_EMPTY_SEAT:
                # money each player has available
                playerMoney = packet_received_from_server["Players"][player][COMM_PACKET_money_available]
                self._win.setUiPlayerMoneyCurrency(player=player, ammount=playerMoney)
                # dealer / small blind / big blind icon
                dealer_icon_name = packet_received_from_server["Players"][player][COMM_PACKET_dealer_icon]
                self._win.setUiDealerIcons(player=player, dealer_icon_name=dealer_icon_name)
                # action that the player took
                player_action = packet_received_from_server["Players"][player]


    def update_packet_from_own_ui(self):
        pass
