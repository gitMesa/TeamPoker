
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

DealerFunction = DealerClass(game_rules=game_rules, game_data=game_data)

DealerFunction.start_new_poker_round()
playing_players = DealerFunction.find_playing_players_and_setup_dealer_and_first_blinds()
playing_order = playing_players

testDealer = DealerClass(game_rules=game_rules, game_data=player_game_data)

testDealer.start_new_poker_round()


take_big_blind = True
take_small_blind = True

def main_dealer_loop (take_big_blind, take_small_blind):
    for current_player in playing_order:
        bet_value = game_data["Dealer"]["BetValue"]
        if game_data["PlayersInfo"][current_player][PINFO_status] == STATUS_G_PLAYING:

            cards = game_data["PlayersGame"][current_player][PGAME_playerCards]
            DealerFunction.print_actual_card(cards[0], cards[1], current_player)

            if take_small_blind and game_data["PlayersGame"][current_player][PGAME_blindStatus] == STATUS_G_SMALL_BLIND:
                DealerFunction.player_bet_money(current_player, game_rules[2])
                print(f"Player{current_player} SMALL_BLIND:{game_data}")
                take_small_blind = False

            if take_big_blind and game_data["PlayersGame"][current_player][PGAME_blindStatus] == STATUS_G_BIG_BLIND:
                DealerFunction.player_bet_money(current_player, game_rules[3])
                game_data["Dealer"]["BetValue"] = game_rules[3]
                print(f"Player{current_player} BIG_BLIND:{game_data}")
                take_big_blind = False

            if game_data["PlayersInfo"][current_player][PINFO_actionID] == ACTION_CALL:
                if game_data["PlayersGame"][current_player][PGAME_moneyAvailable] < bet_value:
                    money_left = game_data["PlayersGame"][current_player][PGAME_moneyAvailable]
                    DealerFunction.player_bet_money(current_player, money_left)
                else:
                    DealerFunction.player_bet_money(current_player, bet_value)
                print(f"Player{current_player} ACTION_CALL:{game_data}")

            if game_data["PlayersInfo"][current_player][PINFO_actionID] == ACTION_RAISE:
                raise_value = RaiseValue   # ToDo : connect this to UI
                game_data["PlayersInfo"][current_player][PINFO_actionID] = ACTION_CALL # Todo: remove this in implementation
                bet_value = raise_value
                DealerFunction.player_bet_money(current_player, bet_value)
                print(f"Player{current_player} ACTION_RAISE:{game_data}")

                for i in range (playing_order.index(current_player))
                    playing_order.append(playing_order[0])
                    playing_order.remove(playing_order[0])
                break
    print(f"Everyone called, dealer moved to next step:")

main_dealer_loop(take_big_blind, take_small_blind)
