from TeamPokerMainApp.Multiplayer.NetworkPacket import NetworkPacketClass
from TeamPokerMainApp.GameLogic.Dealer import DealerClass
from TeamPokerMainApp.Common.VariableDefinitions import *

# (StartingMoney, Currency, SmallBlind, BigBlind, BlindIntervalRaise)
game_rules = (float(10.0), 'RON', float(0.25), float(0.50), '10min')

# Get the packet which describes the players information & data
game_data = NetworkPacketClass.get_game_data_for_testing(game_rules[0])

RaiseValue = float(2.0)
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

DealerFunction = DealerClass(game_rules=game_rules, game_data=game_data)

DealerFunction.start_new_poker_round()
playing_players = DealerFunction.find_playing_players_and_setup_dealer_and_first_blinds()


print(game_data)

def main_dealer_loop (starting_player):
    current_player = starting_player
        while True:
            current_player += 1
            if current_player == MAX_CLIENTS:
            current_player = 0
            bet_value = game_data["Dealer"]["BetValue"]
            if game_data["PlayersInfo"][current_player][PINFO_status] == STATUS_G_PLAYING:

                cards = game_data["PlayersGame"][current_player][PGAME_playerCards]
                DealerFunction.print_actual_card(cards[0], cards[1], current_player)

                if game_data["PlayersGame"][current_player][PGAME_blindStatus] == STATUS_G_SMALL_BLIND:
                    DealerFunction.player_bet_money(current_player, game_rules[2])
                    print(f"Player{current_player} SMALL_BLIND:{game_data}")

                if game_data["PlayersGame"][current_player][PGAME_blindStatus] == STATUS_G_BIG_BLIND:
                    DealerFunction.player_bet_money(current_player, game_rules[3])
                    game_data["Dealer"]["BetValue"] = game_rules[3]
                    print(f"Player{current_player} BIG_BLIND:{game_data}")

                if game_data["PlayersInfo"][current_player][PINFO_actionID] == ACTION_CALL:
                    if game_data["PlayersGame"][current_player][PGAME_moneyAvailable] < bet_value:
                        money_left = game_data["PlayersGame"][current_player][PGAME_moneyAvailable]
                        DealerFunction.player_bet_money(current_player, money_left)
                    else:
                        DealerFunction.player_bet_money(current_player, bet_value)

                if game_data["PlayersInfo"][current_player][PINFO_actionID] == ACTION_RAISE:
                    raise_value = RaiseValue   # ToDo : connect this to UI
                    bet_value = raise_value
                    DealerFunction.player_bet_money(current_player, bet_value)