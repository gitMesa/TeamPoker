from TeamPokerMainApp.Multiplayer.NetworkPacket import NetworkPacketClass
from TeamPokerMainApp.GameLogic.Dealer import DealerClass

net_packet = NetworkPacketClass()
game_data = net_packet.get_game_data()

# (StartingMoney, Currency, SmallBlind, BigBlind, BlindIntervalRaise)
game_rules = (float(10.0), 'RON', float(0.25), float(0.50), '10min')


##################################################################
#                       player4
#     player3                             player5
#
#  player2                                    player6
#
#     player1                             player7
#                       player0
###################################################################


##############################################################
# Start testing the Dealer
##############################################################

testDealer = DealerClass(game_rules=game_rules, game_data=game_data)

