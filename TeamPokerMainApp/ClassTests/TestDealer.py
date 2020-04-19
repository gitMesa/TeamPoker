from TeamPokerMainApp.Multiplayer.NetworkPacket import NetworkPacketClass
from TeamPokerMainApp.Common.VariableDefinitions import *
from TeamPokerMainApp.GameLogic.Dealer import DealerClass


class TestDealerClass:

    def __init__(self):

        # (StartingMoney, Currency, SmallBlind, BigBlind, BlindIntervalRaise)
        self.game_rules = (float(10.0), 'RON', float(0.25), float(0.50), '10min')

        # Get the packet which describes the players information & data
        self.game_data = NetworkPacketClass.get_game_data_for_testing(game_rules[0])

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

        self.DealerFunction = DealerClass(game_rules=game_rules, game_data=game_data)

        self.DealerFunction.start_new_poker_round()
        self.playing_players = self.DealerFunction.find_playing_players_and_setup_dealer_and_first_blinds()
        self.playing_order = self.playing_players


        self.take_big_blind = True
        self.take_small_blind = True

    def run_dealer_test_order(self):
        self.main_dealer_loop()

    def main_dealer_loop (self):
        for current_player in self.playing_order:
            bet_value = self.game_data["Dealer"]["BetValue"]
            if game_data["PlayersInfo"][current_player][PINFO_status] == STATUS_PLAYER_PLAYING:

                cards = self.game_data["PlayersGame"][current_player][PGAME_playerCards]
                self.DealerFunction.print_actual_card(cards[0], cards[1], current_player)

                if self.take_small_blind and self.game_data["PlayersGame"][current_player][PGAME_blindStatus] == STATUS_is_SMALL_BLIND:
                    self.DealerFunction.player_bet_money(current_player, game_rules[2])
                    print(f"Player{current_player} SMALL_BLIND:{self.game_data}")
                    self.take_small_blind = False

                if self.take_big_blind and self.game_data["PlayersGame"][current_player][PGAME_blindStatus] == STATUS_is_BIG_BLIND:
                    self.DealerFunction.player_bet_money(current_player, self.game_rules[3])
                    self.game_data["Dealer"]["BetValue"] = self.game_rules[3]
                    print(f"Player{current_player} BIG_BLIND:{self.game_data}")
                    self.take_big_blind = False

                if self.game_data["PlayersInfo"][current_player][PINFO_actionID] == ACTION_CALL:
                    if self.game_data["PlayersGame"][current_player][PGAME_moneyAvailable] < bet_value:
                        money_left = self.game_data["PlayersGame"][current_player][PGAME_moneyAvailable]
                        self.DealerFunction.player_bet_money(current_player, money_left)
                    else:
                        self.DealerFunction.player_bet_money(current_player, bet_value)
                    print(f"Player{current_player} ACTION_CALL:{self.game_data}")

                if self.game_data["PlayersInfo"][current_player][PINFO_actionID] == ACTION_RAISE:
                    raise_value = self.RaiseValue   # ToDo : connect this to UI
                    self.game_data["PlayersInfo"][current_player][PINFO_actionID] = ACTION_CALL # Todo: remove this in implementation
                    bet_value = raise_value
                    self.DealerFunction.player_bet_money(current_player, bet_value)
                    print(f"Player{current_player} ACTION_RAISE:{self.game_data}")

                    for i in range (self.playing_order.index(current_player))
                        self.playing_order.append(self.playing_order[0])
                        self.playing_order.remove(self.playing_order[0])
                    break
        print(f"Everyone called, dealer moved to next step:")


miroTest = TestDealerClass()
miroTest.run_dealer_test_order()