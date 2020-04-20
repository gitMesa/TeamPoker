from TeamPokerMainApp.Multiplayer.NetworkPacket import NetworkPacketClass
from TeamPokerMainApp.GameLogic.HandEvaluator import HandEvaluatorClass
from TeamPokerMainApp.Common.VariableDefinitions import *
import numpy as np

##################################################################
#                       player4
#     player3                             player5
#
#  player2                                    player6
#
#     player1                             player7
#                       player0
###################################################################


class DealerClass(HandEvaluatorClass):

    def __init__(self, game_rules, deck_instance):
        self._packet = NetworkPacketClass()
        self._deck = deck_instance
        self._deck.init_deck()
        self.game_rules = game_rules
        self.game_data = dict()
        self.dealer_step = DEALER_WAITING_FOR_GAME_START
        self.dealer_status = DEALER_thinks_GAME_is_PAUSED
        self.game_status_text = ''

    def get_dealer_game_data(self):
        return self.game_data

    def set_data_to_dealer_game_data(self, update):
        self.game_data = update

    #################################################################################
    # Dealer Logic                                                                  #
    #################################################################################

    def dealer_evaluate_next_step(self):
        if self.dealer_status is DEALER_thinks_GAME_is_PLAYING:

            if self.dealer_step is DEALER_WAITING_FOR_GAME_START:
                self.set_status_message_and_update_history('Waiting for game to start!')

            elif self.dealer_step is DEALER_NEW_GAME:
                self.set_status_message_and_update_history('New game started!')
                self.round = ROUND_PRE_FLOP
                self.clear_cards_on_table_and_pot()
                self.deck = self._deck.shuffle_deck()
                self._deck.print_shuffled_deck(self.deck)  # TODO: remove
                self.player_order = self.find_playing_players_and_setup_dealer_and_first_blinds()
                self.game_data["Dealer"]["BetValue"] = self.game_data["Dealer"]["BigBlind"]
                # Give cards to playing players
                for card_index in range(NUMBER_OF_CARDS_IN_HAND):
                    for player in self.player_order:
                        self.game_data["Player"][player]["PlayerCards"][card_index] = self.get_top_card()
                self.dealer_step = DEALER_WAIT_FOR_PLAYER_ACTION

            elif self.dealer_step is DEALER_WAIT_FOR_PLAYER_ACTION:
                bet_value = self.game_data["Dealer"]["BetValue"]
                currency = self.game_data["Dealer"]["Currency"]
                player = self.game_data["Dealer"]["NextDecision"]
                playerName = self.game_data["Player"][player]["Name"]
                if self.game_data["Player"][player]["GameAction"] == ACTION_UNDECIDED:
                    self.set_status_message_and_update_history(f'Waiting for {playerName} to decide...')
                # If the decision is to CALL
                if self.game_data["Player"][player]["GameAction"] == ACTION_CALL:
                    # Check if the player has enough money to do a minimum call
                    if self.game_data["Player"][player]["MoneyAvailable"] < bet_value:
                        money_left = self.game_data["Player"][player]["MoneyAvailable"]
                        self.player_bet_money(player, money_left)
                        self.set_status_message_and_update_history(f'{playerName} went All In with {money_left} {currency}')
                    else:
                        self.player_bet_money(player, bet_value)
                        self.set_status_message_and_update_history(f'{playerName} Call {bet_value} {currency}')

                    # If the current player is the last to call, go to the next round
                    if self.player_order.index(player) == self.player_order[-1]:
                        self.dealer_step = DEALER_HANDLE_NEXT_ROUND
                        self.game_data["Dealer"]["Dealer"]["NextDecision"] = self.player_order[0]
                    else:
                        # otherwise increment the next decision to the next playing player
                        self.game_data["Dealer"]["NextDecision"] = self.player_order.index(player) + 1
                    print(f"Player{player} ACTION_CALL.")

                if self.game_data["Player"][player]["GameAction"] == ACTION_RAISE:
                    # Get the amount the player raised to
                    raise_value = self.game_data["Player"][player]["BetAmount"]
                    # Reset that amount to 0
                    self.game_data["Player"][player]["BetAmount"] = 0.0
                    # Bet that amount
                    self.player_bet_money(player, raise_value)
                    # Roll the playing order again because everyone else needs to take a decision again.
                    for i in range(self.player_order.index(player)):
                        self.player_order.append(self.player_order[0])
                        self.player_order.remove(self.player_order[0])
                    # The first player in the new rolled order will be the one that raised, so the next decision comes to the second player.
                    self.game_data["Dealer"]["NextDecision"] = self.player_order[1]

            elif self.dealer_step is DEALER_HANDLE_NEXT_ROUND:
                if self.round is ROUND_PRE_FLOP:
                    self.dealer_step = DEALER_WAIT_FOR_PLAYER_ACTION
                    self.round = ROUND_FLOP
                    self.set_status_message_and_update_history(f'FLOP Round.')
                    self.card_round_flop()
                elif self.round is ROUND_FLOP:
                    self.dealer_step = DEALER_WAIT_FOR_PLAYER_ACTION
                    self.round = ROUND_TURN
                    self.set_status_message_and_update_history(f'TURN Round.')
                    self.card_round_turn()
                elif self.round is ROUND_TURN:
                    self.dealer_step = DEALER_WAIT_FOR_PLAYER_ACTION
                    self.round = ROUND_RIVER
                    self.set_status_message_and_update_history(f'RIVER Round.')
                    self.card_round_river()
                else:
                    self.round = ROUND_END
                    self.set_status_message_and_update_history(f'Betting Ended. Evaluating Hands.')
                    self.evaluate_hands()
                    self.dealer_end_game()
                    # TODO: do finish game stuff
        elif self.dealer_status is DEALER_thinks_GAME_is_PAUSED:
            self.set_status_message_and_update_history('Game is Paused!')
        elif self.dealer_status is DEALER_thinks_GAME_is_ENDING:
            self.set_status_message_and_update_history('Game has Ended!')
        else:
            print('ERROR: dealer_evaluate_next_step @ dealer_status')

    def find_playing_players_and_setup_dealer_and_first_blinds(self):
        playing_players = []  # Empty list
        for player in range(MAX_CLIENTS):
            if self.game_data["Player"][player]["GameStatus"] is GAME_STATUS_PLAYER_PLAYING:
                # add them to the list of currently playing players
                playing_players.append(player)
                # and reset all their dealer / blind statuses
                self.game_data["Player"][player]["DealerStatus"] = TABLE_STATUS_is_NORMAL_PLAYER
                self.game_data["Player"][player]["BlindStatus"] = TABLE_STATUS_is_NORMAL_PLAYER
        # Dealer Small Big
        if len(playing_players) >= 3:
            self.game_data["Player"][playing_players[0]]["DealerStatus"] = TABLE_STATUS_is_DEALER
            self.game_data["Player"][playing_players[1]]["BlindStatus"] = TABLE_STATUS_is_SMALL_BLIND
            self.game_data["Player"][playing_players[2]]["BlindStatus"] = TABLE_STATUS_is_BIG_BLIND
            if len(playing_players) == 3:  # With 3 players it goes Dealer Small Big and then Dealer takes the next step.
                self.game_data["Dealer"]["NextDecision"] = playing_players[0]
            else:  # otherwise the 4th player takes the next step
                self.game_data["Dealer"]["NextDecision"] = playing_players[3]
        elif len(playing_players) == 2:
            self.game_data["Player"][playing_players[0]]["DealerStatus"] = TABLE_STATUS_is_DEALER
            self.game_data["Player"][playing_players[1]]["BlindStatus"] = TABLE_STATUS_is_SMALL_BLIND
            self.game_data["Player"][playing_players[0]]["BlindStatus"] = TABLE_STATUS_is_BIG_BLIND
            self.game_data["Dealer"]["NextDecision"] = playing_players[1]
        else:
            self.game_status_text = "Game doesn't have enough players to start a game."
            # the statuses are already set to NONE so no modification of statuses is needed
        print(f'Number of playing players: {len(playing_players)}')
        return playing_players

    def dealer_start_the_game(self):
        self.dealer_status = DEALER_thinks_GAME_is_PLAYING
        self.dealer_step = DEALER_NEW_GAME

    def set_status_message_and_update_history(self, status_message):
        self.game_data["Dealer"]["GameStatus"] = status_message
        # TODO: Add update to history of plays

    def clear_cards_on_table_and_pot(self):
        self.game_data["Dealer"]["TableCards"] = [NO_CARD, NO_CARD, NO_CARD, NO_CARD, NO_CARD]
        self.game_data["Dealer"]["TablePot"] = 0.0
        for player in range(1, MAX_CLIENTS):
            self.game_data["Player"][player]["PlayerCards"] = [NO_CARD, NO_CARD]

    def player_bet_money(self, player, bet_value):
        self.game_data["Player"][player]["MoneyAvailable"] -= bet_value
        self.game_data["Dealer"]["TablePot"] += bet_value

    def card_round_flop(self):
        self.burn_a_card()
        for card in range(NUMBER_OF_CARDS_ON_FLOP):
            self.add_card_on_table(card, self.get_top_card())

    def card_round_turn(self):
        self.burn_a_card()
        self.add_card_on_table(CARD_INDEX_TURN, self.get_top_card())

    def card_round_river(self):
        self.burn_a_card()
        self.add_card_on_table(CARD_INDEX_RIVER, self.get_top_card())

    def burn_a_card(self):
        self.get_top_card()
        self.game_data["BurnedCards"] += 1

    def get_top_card(self):
        topCard = self.deck[CARD_INDEX_TOP_CARD]
        self.deck = np.delete(self.deck, CARD_INDEX_TOP_CARD)
        return topCard

    def add_money_to_pot(self, ammount):
        self.game_data["Dealer"]["TablePot"] += float(ammount)

    def add_card_on_table(self, card_number_on_table, card_index_from_deck):
        self.game_data["Dealer"]["TableCards"][card_number_on_table] = card_index_from_deck

    def set_game_rules(self):
        # game_rules = (starting_ammount, currency, small_blind, big_blind, blind_interval)
        for player in range(0, MAX_CLIENTS):
            self.game_data["Player"][player]["MoneyAvailable"] = self.game_rules[0]

    def set_dealer_status(self, status):
        self.dealer_status = status

    def dealer_end_game(self):
        pass

    def evaluate_hands(self):
        #TODO: victor leaga magia :)
        pass

