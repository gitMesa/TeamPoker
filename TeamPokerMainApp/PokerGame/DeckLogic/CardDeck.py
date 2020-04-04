from TeamPokerMainApp.Common.VariableDefinitions import *
import numpy as np


class CardDeckClass:

    def init_deck(self):
        self.deckDefinition = dict()
        self.deckDefinitionEvaluation = dict()

        i = 0
        for color in range(len(CARD_SUITS)):
            for card in range(len(CARD_SIGNS)):
                self.deckDefinition[i] = f'{CARD_SIGNS[card]}{CARD_SUITS[color]}'
                self.deckDefinitionEvaluation[i] = (CARD_SIGNS_INDEX[card], CARD_SUITS_TEXT[color])
                i += 1

        print(self.deckDefinition)
        print(self.deckDefinitionEvaluation)

    # create an array of 52 cards(as indexes) and shuffle it
    def shuffle_deck(self):
        shuffledDeck = np.arange(NUMBER_OF_CARDS_IN_DECK)
        np.random.shuffle(shuffledDeck)
        return shuffledDeck

    # get the card name/color based on input index
    def get_card_name_from_card_number(self, index):
        return self.deckDefinition[index]

    def get_card_number_from_card_id(self, index):
        return self.deckDefinitionEvaluation[index]

    def print_shuffled_deck(self, shuffledDeckIndexes):
        prnt = 'Shuffled Deck: '
        for i in shuffledDeckIndexes:
            prnt += self.get_card_name_from_card_number(i)
            prnt += ' '
        print(prnt)
