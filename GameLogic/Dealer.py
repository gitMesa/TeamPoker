from Common.VariableDefinitions import *

class Dealer:

    def __init__(self):
        self.cardsOnTable = [NO_CARD, NO_CARD, NO_CARD, NO_CARD, NO_CARD]
        self.pot = 0

    def addMoneyToPot(self, ammount):
        self.pot += ammount

    def clearCardsOnTheTableAndPot(self):
        self.cardsOnTable = [NO_CARD, NO_CARD, NO_CARD, NO_CARD, NO_CARD]
        self.pot = 0

    def setCardsOnTheTable(self, cardNumberOnTable, cardIndexFromDeck):
        self.cardsOnTable[cardNumberOnTable] = cardIndexFromDeck

    def getCardsOnTheTable(self):
        return self.cardsOnTable
