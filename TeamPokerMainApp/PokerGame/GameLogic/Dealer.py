from TeamPokerMainApp.PokerGame.GameLogic.HandEvaluator import HandEvaluatorClass
from TeamPokerMainApp.PokerGame.DeckLogic.CardDeck import CardDeckClass
from TeamPokerMainApp.Common.VariableDefinitions import *
import numpy as np


class DealerClass(HandEvaluatorClass, CardDeckClass):

    def __init__(self, game_rules, network_packet):
        self.init_deck()
        self.game_rules = game_rules
        self.table_info = network_packet
        self.clear_cards_on_table_and_pot()

    def getTableInfo(self):
        return self.table_info

    def new_poker_round(self):
        self.clear_cards_on_table_and_pot()
        self.deck = self.shuffle_deck()
        self.print_shuffled_deck(self.deck)
        # start giving cards to players
        for card_index in range(NUMBER_OF_CARDS_IN_HAND):
            for player in range(NO_OF_CLIENTS):
                if self.table_info["Players"][COMM_PACKET_status] is STATUS_PLAYING:
                    self.give_cards_to_playing_players(player, card_index, self.get_top_card())

    def give_cards_to_playing_players(self, player, card_index, card):
        self.table_info["Players"][player][COMM_PACKET_player_cards][card_index] = card

    def clear_cards_on_table_and_pot(self):
        self.table_info["TableCards"] = [NO_CARD, NO_CARD, NO_CARD, NO_CARD, NO_CARD]
        self.table_info["TablePot"] = 0.0
        for player in range(1, NO_OF_CLIENTS):
            playerData = list(self.table_info["Players"][player])
            playerData[COMM_PACKET_player_cards] = [NO_CARD, NO_CARD]
            self.table_info["Players"][player] = tuple(playerData)

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
        self.table_info["BurnedCards"] += 1

    def get_top_card(self):
        topCard = self.deck[CARD_INDEX_TOP_CARD]
        self.deck = np.delete(self.deck, CARD_INDEX_TOP_CARD)
        return topCard

    def add_money_to_pot(self, ammount):
        self.table_info["TablePot"] += float(ammount)

    def add_card_on_table(self, card_number_on_table, card_index_from_deck):
        self.table_info["TableCards"][card_number_on_table] = card_index_from_deck

    def evaluate_hands(self):
        #TODO: victor leaga magia :)
        pass

