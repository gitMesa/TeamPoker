from TeamPokerMainApp.GameLogic.HandEvaluator import HandEvaluatorClass
from TeamPokerMainApp.GameLogic.CardDeck import CardDeckClass
from TeamPokerMainApp.Common.VariableDefinitions import *
import numpy as np


class DealerClass(HandEvaluatorClass, CardDeckClass):

    def __init__(self, data):
        self.game_init = False
        self.game_data = data
        self.dealer_step = DEALER_INIT_GAME
        self.deck = list()
        self.player_decision_order = list()
        self.card_order = list()

    def dealer_evaluate_next_step(self):
        players_playing = self.dealer_figure_out_if_we_can_play()
        client0overwrite = self.game_data[CLIENT_SRV][PC_ClientOverwrite]

        if self.game_data[DL_isGamePlaying] is GAME_is_PLAYING or client0overwrite is Overwrite_START_GAME:

            # Before starting a new game.
            if self.dealer_step is DEALER_INIT_GAME:
                # Nothing much for now.
                self.dealer_step = DEALER_NEW_GAME

            # After starting a fresh new game.
            elif self.dealer_step is DEALER_NEW_GAME:
                self.clear_cards_on_table_and_pot()
                self.round = ROUND_PRE_FLOP
                self.set_status_message_and_update_history('New game started!')
                # Count the number of playing players. Get the playing order list.
                # Setup dealer, small and big blinds, and the next decision maker.
                self.player_decision_order, self.card_order = self.dealer_find_new_playing_players_and_setup_dealer_and_blinds()
                # The next decision maker is the first one in the new player_decision_order list
                self.game_data[DL_idNextDecision] = self.player_decision_order[0]
                # Reset minimum bet to BigBlind Value at start of a new round
                self.game_data[DL_MinBet] = self.game_data[DL_BigBlind]
                # get new shuffled deck
                self.deck = self.shuffle_deck()
                self.print_shuffled_deck(self.deck)  # TODO: remove
                # Give cards to playing players in order after dealer
                self.dealer_give_cards_to_players()
                # Done. Wait for players to take decisions.
                self.dealer_step = DEALER_WAIT_FOR_PLAYER_ACTION

            elif self.dealer_step is DEALER_WAIT_FOR_PLAYER_ACTION:
                # Get the info about who we should wait for
                player = self.game_data[DL_idNextDecision]
                player_name = self.game_data[player][PC_Name]
                min_bet_value = self.game_data[DL_MinBet]
                currency = self.game_data[DL_Currency]

                if self.game_data[player][PC_idPlayerAction] == ACTION_UNDECIDED:
                    self.set_status_message_and_update_history(f'Waiting for {player_name} to decide...')

                # If the decision is to CALL
                elif self.game_data[player][PC_idPlayerAction] == ACTION_CALL:
                    # Check if the player has enough money to do a minimum call
                    if self.game_data[player][PS_MoneyAvailable] < min_bet_value:
                        money_left = self.game_data[player][PS_MoneyAvailable]
                        self.player_bet_money(player, money_left)
                        self.game_data[player][PS_textPlayerTable] = f'All In {money_left} {currency}.'
                        self.set_status_message_and_update_history(f'{player_name} went All In with {money_left} {currency}')
                    else:
                        self.player_bet_money(player, min_bet_value)
                        self.game_data[player][PS_textPlayerTable] = f'Call {min_bet_value} {currency}.'
                        self.set_status_message_and_update_history(f'{player_name} Called {min_bet_value} {currency}')
                    self.dealer_increment_and_update_next_decision_player(player=player)

                elif self.game_data[player][PC_idPlayerAction] == ACTION_RAISE:
                    # Get the amount the player raised, and reset his info to 0
                    raise_value = self.game_data[player][PC_BetAmount]
                    if raise_value == self.game_data[player][PS_MoneyAvailable]:
                        self.game_data[player][PS_textPlayerTable] = f'All In {raise_value} {currency}.'
                        self.set_status_message_and_update_history(f'{player_name} went All In with {raise_value} {currency}')
                    else:
                        self.game_data[player][PS_textPlayerTable] = f'Raised {raise_value} {currency}.'
                        self.set_status_message_and_update_history(f'{player_name} Raised to {raise_value} {currency}')
                    # Bet that amount
                    self.player_bet_money(player, raise_value)
                    # Roll the playing order again because everyone else needs to take a decision again.
                    # If I am the one who raises, and everyone calls, i won't get to talk again.
                    # So put me first in the player_decision_order_list and let the list end.
                    for i in range(self.player_decision_order.index(player)):
                        self.player_decision_order.append(self.player_decision_order[0])
                        self.player_decision_order.remove(self.player_decision_order[0])
                    # The first player in the new rolled order will be the one that raised, so the next decision comes to the second player.
                    self.game_data[DL_idNextDecision] = self.player_decision_order[1]
                    # Clear all table texts for all players to prepare for the new round
                    for player_id in range(MAX_CLIENTS):
                        if player_id != player:  # don't clear text for the player who raised.
                            self.game_data[player_id][PS_textPlayerTable] = ''

                elif self.game_data[player][PC_idPlayerAction] == ACTION_FOLD:
                    self.set_status_message_and_update_history(f'{player_name} Folded.')
                    self.dealer_increment_and_update_next_decision_player(player=player)

                else:
                    print('self.dealer_step is DEALER_WAIT_FOR_PLAYER_ACTION -> This should never be reached.')
                    pass
                # Reset Player Action
                self.game_data[player][PC_idPlayerAction] = ACTION_UNDECIDED

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
        elif self.game_data[DL_isGamePlaying] is GAME_is_PAUSED or client0overwrite is Overwrite_PAUSE_GAME:
            self.set_status_message_and_update_history(f'Game is Paused! {players_playing} want to play!')
        elif self.game_data[DL_isGamePlaying] is GAME_is_ENDING or client0overwrite is Overwrite_END_GAME:
            self.set_status_message_and_update_history('Game has Ended!')
        else:
            print('ERROR: dealer_evaluate_next_step @ dealer_status')

    def dealer_figure_out_if_we_can_play(self):
        # Count the number of players, and the number that are actually want to play this round.
        players_connected_and_playing = 0
        for player in range(MAX_CLIENTS):
            if self.game_data[player][PS_ConnectionStatus] is CONN_STATUS_CONNECTED:
                if self.game_data[player][PC_isPlayerPlaying] is True:
                    players_connected_and_playing += 1
        return players_connected_and_playing

    def dealer_find_new_playing_players_and_setup_dealer_and_blinds(self):
        playing_players = [0, 1, 2, 3, 4, 5, 6, 7]  # default list that contains all player indexes
        # now remove all the players that are not playing. The remaining list will have the new dealer at index 0.
        for player in range(MAX_CLIENTS):
            # clear all statuses for the players
            self.game_data[player][PS_isDealer] = TABLE_STATUS_is_NORMAL_PLAYER
            self.game_data[player][PS_isBlind] = TABLE_STATUS_is_NORMAL_PLAYER
            self.game_data[player][PS_textPlayerTable] = ''
            # if he is not playing remove him from the card list
            if self.game_data[player][PC_isPlayerPlaying] is False:
                playing_players.remove(player)

        # Find last game dealer.
        old_dealer_index = self.dealer_find_last_game_dealer_player()
        # Find the next dealer which should be this round
        dealer_player = self.find_next_player_in_list(list_of_players=playing_players, current_player=old_dealer_index)
        # Find the small blind
        small_blind_player = self.find_next_player_in_list(list_of_players=playing_players, current_player=dealer_player)
        # Find the big blind player
        big_blind_player = self.find_next_player_in_list(list_of_players=playing_players, current_player=small_blind_player)

        self.game_data[playing_players[dealer_player]][PS_isDealer] = TABLE_STATUS_is_DEALER
        # set small blind and take his money
        self.game_data[playing_players[small_blind_player]][PS_isBlind] = TABLE_STATUS_is_SMALL_BLIND
        self.player_bet_money(player=small_blind_player, bet_value=self.game_data[DL_BigBlind]/2)
        # set big blind and take his money
        self.game_data[playing_players[big_blind_player]][PS_isBlind] = TABLE_STATUS_is_BIG_BLIND
        self.player_bet_money(player=big_blind_player, bet_value=self.game_data[DL_BigBlind])

        # Roll the player_decision_order_list list until big blind is the last in the list
        decision_order = self.dealer_roll_an_order_list(player_list=playing_players, last_player_index=big_blind_player)
        # roll the card_order until old-dealer is the last player in that list
        card_order = self.dealer_roll_an_order_list(player_list=playing_players, last_player_index=dealer_player)

        return decision_order, card_order

    def dealer_find_last_game_dealer_player(self):
        old_dealer_index = 99  # invalid value
        isDealer_occurences = 0
        for player in range(MAX_CLIENTS):
            if self.game_data[player][PS_isDealer] is TABLE_STATUS_is_DEALER:
                isDealer_occurences += 1
                old_dealer_index = player
        # Fail-safe, if more then 1 occurrence is seen program should crash
        if isDealer_occurences > 1:
            old_dealer_index = 99  # invalid value
        return old_dealer_index

    def dealer_give_cards_to_players(self):
        for card_index in range(NUMBER_OF_CARDS_IN_HAND):
            for player in self.card_order:
                self.game_data[player][PS_PlayerCards][card_index] = self.get_top_card()

    def dealer_increment_and_update_next_decision_player(self, player):
        # If the current player is the last to call, go to the next round
        if player == self.player_decision_order[-1]:
            self.game_data[DL_idNextDecision] = self.player_decision_order[0]
            self.dealer_step = DEALER_HANDLE_NEXT_ROUND
            # Clear all decisions/statuses for all players to prepare for the new round
            for player in range(MAX_CLIENTS):
                self.game_data[player][PS_textPlayerTable] = ''
        else:
            # otherwise increment the next decision to the next playing player
            self.game_data[DL_idNextDecision] = self.player_decision_order.index(player) + 1

    def set_status_message_and_update_history(self, status_message):
        self.game_data[DL_textTableCenter] = status_message

    def clear_cards_on_table_and_pot(self):
        self.game_data[DL_TableCards] = [NO_CARD, NO_CARD, NO_CARD, NO_CARD, NO_CARD]
        self.game_data[DL_TablePot] = 0.0
        for player in range(1, MAX_CLIENTS):
            self.game_data[player][PS_PlayerCards] = [NO_CARD, NO_CARD]

    def player_bet_money(self, player, bet_value):
        self.game_data[player][PC_BetAmount] = 0.0
        self.game_data[player][PS_MoneyAvailable] -= bet_value
        self.game_data[DL_TablePot] += bet_value

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
        self.game_data[DL_noBurnedCards] += 1

    def get_top_card(self):
        topCard = self.deck[CARD_INDEX_TOP_CARD]
        self.deck = np.delete(self.deck, CARD_INDEX_TOP_CARD)
        return topCard

    def dealer_roll_an_order_list(self, player_list, last_player_index):
        input_list = list.copy(player_list)  # To dereference the original list
        while input_list[-1] != last_player_index:
            input_list.append(input_list[0])
            input_list.remove(input_list[0])
        return input_list

    def add_money_to_pot(self, amount):
        self.game_data[DL_TablePot] += float(amount)

    def add_card_on_table(self, card_number_on_table, card_index_from_deck):
        self.game_data[DL_TableCards][card_number_on_table] = card_index_from_deck

    def find_next_player_in_list(self, list_of_players, current_player):
        next_dealer = 0
        for i in list_of_players:
            if i > current_player:
                next_dealer = i
                break
        return next_dealer

    def dealer_end_game(self):
        pass

    def evaluate_hands(self):
        #TODO: victor leaga magia :)
        pass

