from TeamPokerMainApp.PokerGame.GameLogic.HandEvaluator import HandEvaluatorClass
from TeamPokerMainApp.PokerGame.DeckLogic.CardDeck import CardDeckClass
from TeamPokerMainApp.Common.VariableDefinitions import *


class DealerClass(HandEvaluatorClass, CardDeckClass):

    def __init__(self):
        self.cardsOnTable = []
        self.pot = float
        self.clear_cards_on_table_and_pot()
        self.init_deck()

    def clear_cards_on_table_and_pot(self):
        self.cardsOnTable = [NO_CARD, NO_CARD, NO_CARD, NO_CARD, NO_CARD]
        self.pot = 0.0

    def add_money_to_pot(self, ammount):
        self.pot += ammount

    def add_card_on_table(self, cardNumberOnTable, cardIndexFromDeck):
        self.cardsOnTable[cardNumberOnTable] = cardIndexFromDeck

    def get_cards_from_table(self):
        return self.cardsOnTable

    def evaluate_hands(self):
        pass

    def give_cards_to_players(self, number_of_players_playing, player_index_who_is_dealer):
        pass

