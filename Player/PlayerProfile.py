from Common.VariableDefinitions import *

class PlayerProfile:

    def __init__(self):
        self.inGameStatus = STATUS_SIT_OUT
        self.moneyAvailable = 0
        self.name = 'Empty Seat'
        self.cardsInHand = [99, 99]

    def clearPlayer(self):
        self.moneyAvailable = 0
        self.name = 'Empty Seat'
        self.cardsInHand = [99, 99]

    def createNewPlayer(self, name, money):
        self.moneyAvailable = money
        self.name = name
        self.inGameStatus = STATUS_PLAYING

    def setCardsInPlayerHand(self, cardNumberInHand, cardIndexFromDeck):
        self.cardsInHand[cardNumberInHand] = cardIndexFromDeck

    def getPlayingStatus(self):
        return self.inGameStatus

    def getCardsInPlayerHand(self):
        return self.cardsInHand

    def addMoneyToPlayer(self, ammount):
        self.moneyAvailable += ammount

    def removeMoneyFromPlayer(self, ammount):
        self.moneyAvailable -= ammount
