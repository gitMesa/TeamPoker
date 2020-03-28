from Common.VariableDefinitions import *
import numpy as np


class CardDeck:

    def __init__(self):
        self.cardNumbers = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
        self.cardNumbersEvaluation = [ 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        self.cardColors = ['♡', '♤', '♧', '♢']
        self.cardColorsEvaluation = ['heart', 'spade', 'club', 'diamond']
        self.deckDefinition = dict()
        self.deckDefinitionEvaluation = dict()

        i = 0
        for color in range(len(self.cardColors)):
            for card in range(len(self.cardNumbers)):
                self.deckDefinition[i] = f'{self.cardNumbers[card]}{self.cardColors[color]}'
                self.deckDefinitionEvaluation[i] = (self.cardNumbersEvaluation[card],self.cardColorsEvaluation[color])
                i += 1

        print(self.deckDefinition)
        print(self.deckDefinitionEvaluation)

    # create an array of 52 cards(as indexes) and shuffle it
    def getShuffledDeck(self):
        shuffledDeck = np.arange(NUMBER_OF_CARDS_IN_DECK)
        np.random.shuffle(shuffledDeck)
        return shuffledDeck

    # get the card name/color based on input index
    def getCardNumberTranlation(self, index):
        return self.deckDefinition[index]

    def getCardNumberTranlationEvaluation(self, index):
        return self.deckDefinitionEvaluation[index]

    def printShuffledDeck(self, shuffledDeckIndexes):
        prnt = 'Shuffled Deck: '
        for i in shuffledDeckIndexes:
            prnt += self.getCardNumberTranlation(i)
            prnt += ' '
        print(prnt)
