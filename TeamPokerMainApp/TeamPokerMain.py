from TeamPokerMainApp.Player.PlayerProfile import PlayerProfileClass
from TeamPokerMainApp.PokerGame.PokerGame import PokerGameClass
from TeamPokerMainApp.Common.VariableDefinitions import *


############################################################################################
# Purpose of this class is to create a basic UI asking the user to setup his player profile
#
# 1. Mode Server:

#
############################################################################################

class TeamPokerMain:

    def __init__(self):
        pass

    def create_poker_game_server(self):
        self._PokerGame = PokerGameClass(mode=SERVER)

    def create_poker_game_client(self):
        self._PokerGame = PokerGameClass(mode=CLIENT)

