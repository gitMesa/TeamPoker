from TeamPokerMainApp.Common.VariableDefinitions import *
from TeamPokerMainApp.Player.PlayerProfile import PlayerProfile
from TeamPokerMainApp.GameLogic.CardDeck import CardDeck
from TeamPokerMainApp.GameLogic.Dealer import Dealer
from TeamPokerMainApp.GameLogic.HandEvaluator import HandEvaluator
import numpy as np


class PokerGame:
    numberOfPlayers = 0
    maximumPlayers = 9

    def __init__(self):
        self._dealer = Dealer()
        self._deck = CardDeck()
        self._player0 = PlayerProfile()
        self._player1 = PlayerProfile()
        self._player2 = PlayerProfile()
        self._player3 = PlayerProfile()
        self._player4 = PlayerProfile()
        self._player5 = PlayerProfile()
        self._player6 = PlayerProfile()
        self._player7 = PlayerProfile()
        self._player8 = PlayerProfile()

    def addNewPlayer(self, name, money):
        if self.numberOfPlayers < 8:
            eval(f'self._player{self.numberOfPlayers}.createNewPlayer(name, money)')
            self.numberOfPlayers += 1
        else:
            print('Table is full!')

    def removePlayer(self, playerNumber):
        self.numberOfPlayers -= 1
        eval(f'self._player{playerNumber}.clearPlayer()')

    def newPokerRound(self):
        self._dealer.clearCardsOnTheTableAndPot()
        self.deck = self._deck.get_shuffled_deck()
        self._deck.print_shuffled_deck(self.deck)
        # start giving cards to players
        for card in range(NUMBER_OF_CARDS_IN_HAND):
            for player in range(self.maximumPlayers):
                if eval(f'self._player{player}.getPlayingStatus()') is STATUS_G_PLAYING:
                    eval(f'self._player{player}.setCardsInPlayerHand(card, self.get_top_card())')

    def card_round_flop(self):
        self.get_top_card()  # just removes top card from the deck, to burn it
        for card in range(NUMBER_OF_CARDS_ON_FLOP):
            self._dealer.setCardsOnTheTable(card, self.get_top_card())

    def card_round_turn(self):
        self.get_top_card()  # just removes top card from the deck, to burn it
        self._dealer.setCardsOnTheTable(CARD_INDEX_TURN, self.get_top_card())

    def card_round_river(self):
        self.get_top_card()  # just removes top card from the deck, to burn it
        self._dealer.setCardsOnTheTable(CARD_INDEX_RIVER, self.get_top_card())

    def get_top_card(self):
        topCard = self.deck[CARD_INDEX_TOP_CARD]
        self.deck = np.delete(self.deck, CARD_INDEX_TOP_CARD)
        return topCard

    def printPlayerHands(self):
        for player in range(self.numberOfPlayers):
            printingString = eval(f'self._player{player}.name')
            for item in eval(f'self._player{player}.getCardsInPlayerHand()'):
                printingString += ' '
                printingString += self._deck.get_card_name_from_card_number(item)

            print(printingString)

    def printTableCards(self):
        prnt = ''
        for card in self._dealer.getCardsOnTheTable():
            if card is not NO_CARD:
                prnt += ' '
                prnt += self._deck.get_card_name_from_card_number(card)
        print(prnt)

    def takePlayerCardsPlusTableCards(self, playerID):
        sevenCards = []
        for card in eval(f'self._player{playerID}.getCardsInPlayerHand()'):
            sevenCards.append(self._deck.get_card_number_from_card_id(card))
        for card in self._dealer.getCardsOnTheTable():
            sevenCards.append(self._deck.get_card_number_from_card_id(card))
        return sevenCards

    def evaluatePlayersHands(self):
        print("\nResults:")
        for player in range(self.numberOfPlayers):
            playerName = eval(f'self._player{player}.name')
            sevenCards = self.takePlayerCardsPlusTableCards(player)
            handEvaluator = HandEvaluator(sevenCards, playerName)
            result = handEvaluator.evaluate_hand()
            print(result)


game = PokerGame()
game.addNewPlayer('Victor', 10.0)
game.addNewPlayer('Cornel', 10.0)
game.addNewPlayer('Csaba', 10.0)
game.addNewPlayer('Adi', 10.0)
game.addNewPlayer('Andrei', 10.0)

game.newPokerRound()
print('----')
game.printPlayerHands()
print('----')
print('Flop: ')
game.card_round_flop()
game.printTableCards()
print('Turn: ')
game.card_round_turn()
game.printTableCards()
print('River: ')
game.card_round_river()
game.printTableCards()
game.evaluatePlayersHands()
