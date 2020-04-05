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

    def __init__(self, mode, player_info):
        if mode is SERVER:
            self._GameLogic = DealerClass
            self.PlayerInfo = player_info
        elif mode is CLIENT:
            self.PlayerInfo = player_info
        else:
            print('Somebody fucked up!')

###################################################################
# 1. Mode Server:
#   Shall set up rules for the game. Small/Big Blind, Buy-In Rules, etc.
#   Shall accept connections from Clients.
#   Shall remember the Buy-In / Money of Players and show them in a statistics tab.
#   Shall handle the table/dealer/pot/logic.
#   Shall send cards to Players(Client Mode).
#   Shall receive actions from Players(Client Mode).
###################################################################

    def setup_game_rules(self):
