from TeamPokerMainApp.GameLogic.HandEvaluator import HandEvaluatorClass
from TeamPokerMainApp.GameLogic.CardDeck import CardDeckClass
from TeamPokerMainApp.Common.VariableDefinitions import *
import numpy as np


class DealerClass(HandEvaluatorClass, CardDeckClass):

    def __init__(self, data):
        self.game_data = data
        self.dealer_step = DEALER_INIT_GAME
        self.player_decision_order = list()
        self.card_order = list()

    def dealer_evaluate_next_step(self):
        self.dealer_figure_out_if_we_can_play()
        if self.game_data["Dealer"]["GameState"] is DEALER_thinks_GAME_is_PLAYING:

            if self.dealer_step is DEALER_INIT_GAME:
                self.init_playing_players_and_setup_dealer_and_blinds()

            elif self.dealer_step is DEALER_NEW_GAME:
                self.clear_cards_on_table_and_pot()
                self.round = ROUND_PRE_FLOP
                self.set_status_message_and_update_history('New game started!')
                # Count the number of playing players. Get the playing order list.
                # Setup dealer, small and big blinds, and the next decision maker.
                self.player_decision_order, self.card_order = self.dealer_find_new_playing_players_and_setup_dealer_and_blinds()
                print(f'Playing Order {self.card_order} - Next Decision {self.game_data["Dealer"]["NextDecision"]}')
                # Reset minimum bet to BigBlind Value at start of a new round
                self.game_data["Dealer"]["MinAllowedBet"] = self.game_data["Dealer"]["BigBlind"]
                # Give cards to playing players in order after dealer
                self.dealer_give_cards_to_players()
                # Done. Wait for players to take decisions.
                self.dealer_step = DEALER_WAIT_FOR_PLAYER_ACTION

            elif self.dealer_step is DEALER_WAIT_FOR_PLAYER_ACTION:
                # Get the info about who we should wait for
                player = self.game_data["Dealer"]["NextDecision"]
                player_name = self.game_data["PlayerClient"][player]["Name"]
                min_bet_value = self.game_data["Dealer"]["MinAllowedBet"]
                currency = self.game_data["Dealer"]["Currency"]

                if self.game_data["PlayerClient"][player]["PlayerAction"] == ACTION_UNDECIDED:
                    self.set_status_message_and_update_history(f'Waiting for {player_name} to decide...')

                # If the decision is to CALL
                elif self.game_data["PlayerClient"][player]["PlayerAction"] == ACTION_CALL:
                    # Check if the player has enough money to do a minimum call
                    if self.game_data["PlayerServer"][player]["MoneyAvailable"] < min_bet_value:
                        money_left = self.game_data["Player"][player]["MoneyAvailable"]
                        self.player_bet_money(player, money_left)
                        self.set_status_message_and_update_history(f'{player_name} went All In with {money_left} {currency}')
                    else:
                        self.player_bet_money(player, min_bet_value)
                        self.set_status_message_and_update_history(f'{player_name} Called {bet_value} {currency}')

                    # If the current player is the last to call, go to the next round
                    if self.player_decision_order.index(player) == self.player_decision_order[-1]:
                        self.dealer_step = DEALER_HANDLE_NEXT_ROUND
                        self.game_data["Dealer"]["NextDecision"] = self.player_decision_order[0]
                    else:
                        # otherwise increment the next decision to the next playing player
                        self.game_data["Dealer"]["NextDecision"] = self.player_decision_order.index(player) + 1
                    # Reset Player Action
                    self.game_data["PlayerClient"][player]["PlayerAction"] = ACTION_UNDECIDED

                if self.game_data["PlayerClient"][player]["PlayerAction"] == ACTION_RAISE:
                    # Get the amount the player raised, and reset his info to 0
                    raise_value = self.game_data["PlayerClient"][player]["BetAmount"]
                    self.game_data["PlayerClient"][player]["BetAmount"] = 0.0
                    # Bet that amount
                    self.player_bet_money(player, raise_value)
                    # Roll the playing order again because everyone else needs to take a decision again.
                    # If I am the one who raises, and everyone calls, i won't get to talk again.
                    # So put me first in the player_decision_order_list and let the list end.
                    for i in range(self.player_decision_order.index(player)):
                        self.player_decision_order.append(self.player_decision_order[0])
                        self.player_decision_order.remove(self.player_decision_order[0])
                    # The first player in the new rolled order will be the one that raised, so the next decision comes to the second player.
                    self.game_data["Dealer"]["NextDecision"] = self.player_decision_order[1]
                    # Reset Player Action
                    self.game_data["PlayerClient"][player]["PlayerAction"] = ACTION_UNDECIDED

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
        elif self.game_data["Dealer"]["GameState"] is DEALER_thinks_GAME_is_PAUSED:
            self.set_status_message_and_update_history('Game is Paused!')
        elif self.game_data["Dealer"]["GameState"] is DEALER_thinks_GAME_is_ENDING:
            self.set_status_message_and_update_history('Game has Ended!')
        else:
            print('ERROR: dealer_evaluate_next_step @ dealer_status')

    def dealer_figure_out_if_we_can_play(self):
        # Count the number of players, and the number that are actually want to play this round.
        players_connected_and_playing = 0
        for player in range(MAX_CLIENTS):
            if self.game_data["PlayerServer"][player]["ConnectionStatus"] is CONN_STATUS_CONNECTED:
                if self.game_data["PlayerClient"][player]["PlayerStatus"] is PLAYER_STATUS_player_is_playing:
                    players_connected_and_playing += 1
        if players_connected_and_playing >= 2:
            self.game_data["Dealer"]["GameState"] = DEALER_thinks_GAME_is_PLAYING
        else:
            self.game_data["Dealer"]["GameStatus"] = 'Not enough players want to play. Waiting...'
            self.game_data["Dealer"]["GameState"] = DEALER_thinks_GAME_is_PAUSED

        #TODO: Overwrite from Client0
        # self.game_data["Dealer"]["GameState"] = self.game_data["PlayerClient"][CLIENT_SRV]["Client0ServerOverwrite"]

    def init_playing_players_and_setup_dealer_and_blinds(self):
        player_decision_order_list = []  # Empty list
        for player in range(MAX_CLIENTS):
            if self.game_data["PlayerClient"][player]["PlayerStatus"] is PLAYER_STATUS_player_is_playing:
                # add them to the list of currently playing players
                player_decision_order_list.append(player)
            # Reset all players dealer / blind statuses
            self.game_data["PlayerServer"][player]["isDealer"] = TABLE_STATUS_is_NORMAL_PLAYER
            self.game_data["PlayerServer"][player]["isBlind"] = TABLE_STATUS_is_NORMAL_PLAYER

        if len(player_decision_order_list) >= 3:
            self.game_data["PlayerServer"][player_decision_order_list[0]]["isDealer"] = TABLE_STATUS_is_DEALER
            self.game_data["PlayerServer"][player_decision_order_list[1]]["isBlind"] = TABLE_STATUS_is_SMALL_BLIND
            self.game_data["PlayerServer"][player_decision_order_list[2]]["isBlind"] = TABLE_STATUS_is_BIG_BLIND
            # Roll the player_decision_order_list list until big blind is the last in the list
            self.dealer_roll_playing_order_list(player_order_list=player_decision_order_list, last_player_index=player_decision_order_list[2])

        elif len(player_decision_order_list) == 2:
            self.game_data["PlayerServer"][player_decision_order_list[0]]["isDealer"] = TABLE_STATUS_is_DEALER
            self.game_data["PlayerServer"][player_decision_order_list[1]]["isBlind"] = TABLE_STATUS_is_SMALL_BLIND
            self.game_data["PlayerServer"][player_decision_order_list[0]]["isBlind"] = TABLE_STATUS_is_BIG_BLIND
            # Roll the player_decision_order_list list until big blind is the last in the list
            self.dealer_roll_playing_order_list(player_order_list=player_decision_order_list, last_player_index=player_decision_order_list[0])
        # The next decision maker is the first one in the new player_decision_order_list list
        self.game_data["Dealer"]["NextDecision"] = player_decision_order_list[0]

    def dealer_find_new_playing_players_and_setup_dealer_and_blinds(self):
        # count how many players are playing this game
        dealer_order_list = [0, 1, 2, 3, 4, 5, 6, 7]  # default list that contains all player indexes
        # Find last game dealer.
        old_dealer_index = 99  # invalid value
        isDealer_occurences = 0
        for player in range(MAX_CLIENTS):
            if self.game_data["PlayerServer"][player]["isDealer"] is TABLE_STATUS_is_DEALER:
                isDealer_occurences += 1
                old_dealer_index = player
        # Fail-safe, if more then 1 occurrence is seen program should crash
        if isDealer_occurences > 1:
            old_dealer_index = 99  # invalid value
        # roll the new_playing_players_list until old-dealer is the last player in that list
        dealer_order_list = self.dealer_roll_playing_order_list(dealer_order_list, old_dealer_index)
        # now remove all the players that are not playing. The remaining list will have the new dealer at index 0.
        for player in range(MAX_CLIENTS):
            if self.game_data["PlayerClient"][player]["PlayerStatus"] is not PLAYER_STATUS_player_is_playing:
                dealer_order_list.remove(player)
            # clear also all statuses for the players
            self.game_data["PlayerServer"][player]["isDealer"] = TABLE_STATUS_is_NORMAL_PLAYER
            self.game_data["PlayerServer"][player]["isBlind"] = TABLE_STATUS_is_NORMAL_PLAYER
        # The remaining list will have the new dealer at index 0.
        # Copy the list now because we need 2 versions.
        # Decision order comes after big blind and ends with big blind.
        # Dealer/Card order comes after dealer, and ends with dealer.
        decision_order_list = dealer_order_list

        if len(dealer_order_list) >= 3:
            self.game_data["PlayerServer"][dealer_order_list[0]]["isDealer"] = TABLE_STATUS_is_DEALER
            self.game_data["PlayerServer"][dealer_order_list[1]]["isBlind"] = TABLE_STATUS_is_SMALL_BLIND
            self.game_data["PlayerServer"][dealer_order_list[2]]["isBlind"] = TABLE_STATUS_is_BIG_BLIND
            # Roll the decision_order_list list until big blind is the last in the list
            decision_order_list = self.dealer_roll_playing_order_list(player_order_list=decision_order_list, last_player_index=dealer_order_list[2])

        elif len(dealer_order_list) == 2:
            self.game_data["PlayerServer"][dealer_order_list[0]]["isDealer"] = TABLE_STATUS_is_DEALER
            self.game_data["PlayerServer"][dealer_order_list[1]]["isBlind"] = TABLE_STATUS_is_SMALL_BLIND
            self.game_data["PlayerServer"][dealer_order_list[0]]["isBlind"] = TABLE_STATUS_is_BIG_BLIND
            # Roll the decision_order_list list until big blind is the last in the list
            decision_order_list = self.dealer_roll_playing_order_list(player_order_list=decision_order_list, last_player_index=dealer_order_list[0])
        # The next decision maker is the first one in the new player_decision_order_list list
        self.game_data["Dealer"]["NextDecision"] = decision_order_list[0]
        return decision_order_list, dealer_order_list

    def dealer_give_cards_to_players(self):
        for card_index in range(NUMBER_OF_CARDS_IN_HAND):
            for player in self.card_order:
                self.game_data["PlayerServer"][player]["PlayerCards"][card_index] = self.get_top_card()

    def set_status_message_and_update_history(self, status_message):
        self.game_data["Dealer"]["GameStatus"] = status_message
        # TODO: Add update to history of plays

    def clear_cards_on_table_and_pot(self):
        self.game_data["Dealer"]["TableCards"] = [NO_CARD, NO_CARD, NO_CARD, NO_CARD, NO_CARD]
        self.game_data["Dealer"]["TablePot"] = 0.0
        for player in range(1, MAX_CLIENTS):
            self.game_data["PlayerServer"][player]["PlayerCards"] = [NO_CARD, NO_CARD]

    def player_bet_money(self, player, bet_value):
        self.game_data["PlayerServer"][player]["MoneyAvailable"] -= bet_value
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

    def dealer_roll_playing_order_list(self, player_order_list, last_player_index):
        while player_order_list[-1] != last_player_index:
            player_order_list.append(player_order_list[0])
            player_order_list.remove(player_order_list[0])
        return player_order_list

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

