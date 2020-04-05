from TeamPokerMainApp.PokerGame.GameUI.UiCode.TeamPokerUIController import TeamPokerUIControllerClass
from TeamPokerMainApp.PokerGame.GameLogic.Dealer import DealerClass
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
        self._dealer = DealerClass()

    def setup_game_rules(self):
        pass

###################################################################
# 2. Client Mode:
#   Shall connect to the server providing UserName and UserIcon?
#   Shall receive from Server cards.
#   Shall send to Server Actions.
###################################################################

    def start_poker_client(self):
        pass
