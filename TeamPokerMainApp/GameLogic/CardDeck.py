from TeamPokerMainApp.Common.VariableDefinitions import *
import numpy as np


class CardDeckClass:

    # create an array of 52 cards(as indexes) and shuffle it
    def shuffle_deck(self):
        shuffledDeck = np.arange(NUMBER_OF_CARDS_IN_DECK)
        np.random.shuffle(shuffledDeck)
        return shuffledDeck

    # get the card name/color based on input index
    def get_card_name_from_card_number(self, index):
        deckDefinition = dict()
        i = 0
        for color in range(len(CARD_SUITS)):
            for card in range(len(CARD_SIGNS)):
                deckDefinition[i] = f'{CARD_SIGNS[card]}{CARD_SUITS[color]}'
                i += 1
        if index is NO_CARD:
            name = NO_CARD_IMAGE
        else:
            name = deckDefinition[index]
        return name

    def get_card_number_from_card_id(self, index):
        deckDefinitionEvaluation = dict()
        i = 0
        for color in range(len(CARD_SUITS)):
            for card in range(len(CARD_SIGNS)):
                deckDefinitionEvaluation[i] = (CARD_SIGNS_INDEX[card], CARD_SUITS_TEXT[color])
                i += 1
        return deckDefinitionEvaluation[index]

    def print_shuffled_deck(self, shuffledDeckIndexes):
        prnt = 'Shuffled Deck: '
        for i in shuffledDeckIndexes:
            prnt += self.get_card_name_from_card_number(i)
            prnt += ' '
        print(prnt)
