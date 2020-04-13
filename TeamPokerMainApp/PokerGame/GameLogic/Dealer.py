from TeamPokerMainApp.PokerGame.Multiplayer.NetworkPacket import NetworkPacketClass
from TeamPokerMainApp.PokerGame.GameLogic.HandEvaluator import HandEvaluatorClass
from TeamPokerMainApp.PokerGame.GameLogic.CardDeck import CardDeckClass
from TeamPokerMainApp.Common.VariableDefinitions import *
import numpy as np


class DealerClass(HandEvaluatorClass, CardDeckClass):

    def __init__(self, game_rules, game_data):
        self.init_deck()
        self.game_rules = game_rules
        self._packet = NetworkPacketClass()
        self.game_data = game_data
        self.set_game_rules()
        self.clear_cards_on_table_and_pot()

    def get_dealer_game_data(self):
        return self.game_data

    def set_data_to_dealer_game_data(self, update):
        self.game_data = update

    #################################################################################
    # Dealer Logic                                                                  #
    #################################################################################

    def new_poker_round(self):
        self.deck = self.shuffle_deck()
        self.print_shuffled_deck(self.deck)
        self.clear_cards_on_table_and_pot()
        for card_index in range(NUMBER_OF_CARDS_IN_HAND):
            for player in range(MAX_CLIENTS):
                if self.game_data["PlayersInfo"][player][PINFO_status] is STATUS_PLAYING:
                    self.game_data["PlayersGame"][player][PGAME_playerCards][card_index] = self.get_top_card()

    def clear_cards_on_table_and_pot(self):
        self.game_data["Dealer"]["TableCards"] = [NO_CARD, NO_CARD, NO_CARD, NO_CARD, NO_CARD]
        self.game_data["Dealer"]["TablePot"] = 0.0
        for player in range(1, MAX_CLIENTS):
            self.game_data["PlayersGame"][player][PGAME_playerCards] = [NO_CARD, NO_CARD]

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
            self.game_data["PlayersGame"][player][PGAME_moneyAvailable] = self.game_rules[0]

    def evaluate_hands(self):
        #TODO: victor leaga magia :)
        pass

