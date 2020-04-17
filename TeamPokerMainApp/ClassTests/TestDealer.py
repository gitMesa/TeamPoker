from TeamPokerMainApp.Multiplayer.NetworkPacket import NetworkPacketClass
from TeamPokerMainApp.GameLogic.Dealer import DealerClass

# (StartingMoney, Currency, SmallBlind, BigBlind, BlindIntervalRaise)
game_rules = (float(10.0), 'RON', float(0.25), float(0.50), '10min')

# Get the packet which describes the players information & data
player_game_data = NetworkPacketClass.get_game_data_for_testing(game_rules[0])

##################################################################
#   Start testing the Dealer
##################################################################
#                       player4
#     player3                             player5
#
#  player2                                    player6
#
#     player1                             player7
#                       player0
##################################################################

testDealer = DealerClass(game_rules=game_rules, game_data=player_game_data)

