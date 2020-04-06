from TeamPokerMainApp.PokerGame.GameUI.UiCode.TeamPokerUIController import TeamPokerUIControllerClass
from TeamPokerMainApp.PokerGame.Multiplayer.NetworkPacket import NetworkPacketClass
from TeamPokerMainApp.PokerGame.Multiplayer.Server import MultiplayerServerClass
from TeamPokerMainApp.PokerGame.Multiplayer.Client import ClientClass
from TeamPokerMainApp.PokerGame.GameLogic.Dealer import DealerClass
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
        self._win = TeamPokerUIControllerClass()
        self._comm = NetworkPacketClass()
        self.initConnectButtons()

    def show_main_window(self):
        self._win.showMainWindow()

    def initConnectButtons(self):
        self._win.connectButtonHostGame(self.start_poker_server)
        self._win.connectButtonJoinGame(self.start_poker_client)

###################################################################
# 1. Mode Server:
#   Shall set up rules for the game. Small/Big Blind, Buy-In Rules, etc.
#   Shall accept connections from Clients.
#   Shall remember the Buy-In / Money of Players and show them in a statistics tab.
#   Shall handle the table/dealer/pot/logic.
#   Shall send cards to Players(Client Mode).
#   Shall receive actions from Players(Client Mode).
###################################################################

    def start_poker_server(self):
        self._win.setWindowTitle(self._win.getGameName())
        self._srv = MultiplayerServerClass(ip=self._win.getHostAGameIpAdress(), port=self._win.getHostAGamePortNumber(), packet=self._comm.getCommunicationPacket())
        self._client = ClientClass(ip=self._win.getHostAGameIpAdress(), port=self._win.getHostAGamePortNumber())
        self._dealer = DealerClass(self.get_game_rules())

    def get_game_rules(self):
        starting_ammount = self._win.getStartingAmmount()
        currency = self._win.getCurrency()
        small_blind = self._win.getSmallBlind()
        big_blind = self._win.getBigBlind()
        blind_interval = self._win.getBlindInterval()
        tpl = (starting_ammount, currency, small_blind, big_blind, blind_interval)
        return tpl

###################################################################
# 2. Client Mode:
#   Shall connect to the server providing UserName and UserIcon?
#   Shall receive from Server cards.
#   Shall send to Server Actions.
###################################################################

    def start_poker_client(self):
        self._client = ClientClass(ip=self._win.getJoinAGameIpAdress(), port=self._win.getJoinAGamePortNumber())
        self.request_update_from_server_loop()

    def request_update_from_server_loop(self):
        self.update_timer = QTimer(self._win)
        self.update_timer.start(100)
        self.update_timer.timeout.connect(self.request_update)

    def request_update(self):
        update_from_server = self._client.send_and_receive_update(self._comm.getCommunicationPacket())
        self.update_client_ui_based_on_server_update(update_from_server)

    def update_client_ui_based_on_server_update(self, update_from_server):
        pass
