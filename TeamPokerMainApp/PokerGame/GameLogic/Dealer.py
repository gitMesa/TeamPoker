from TeamPokerMainApp.PokerGame.GameLogic.HandEvaluator import HandEvaluatorClass
from TeamPokerMainApp.PokerGame.GameLogic.CardDeck import CardDeckClass
from TeamPokerMainApp.Common.VariableDefinitions import *
from PyQt5.Qt import QMutex, QMutexLocker
import numpy as np


class DealerClass(HandEvaluatorClass, CardDeckClass):

    def __init__(self, game_rules):
        self.init_deck()
        self.game_rules = game_rules

        # Indexes for field location within the player information.
        # PACKET_table_spot = 0
        # PACKET_status = 1
        # PACKET_name = 2
        # PACKET_icon_id = 3
        # PACKET_action_id = 4
        # PACKET_money_available = 5
        # PACKET_dealer_icon = 6
        # PACKET_player_cards = 7

        self.mutex = QMutex()

        self.PLAYER_DATA_FIELDS = list((int(0), STATUS_EMPTY_SEAT, str(""), str(""), int(0), float(0.0), str(""), [NO_CARD, NO_CARD]))

        self.GAME_DATA_PACKET = {"Dealer": {"TableCards": [NO_CARD, NO_CARD, NO_CARD, NO_CARD, NO_CARD],
                                            "BurnedCards": int(0),
                                            "TablePot": float(0.0)},
                                 "Players": {1: list.copy(self.PLAYER_DATA_FIELDS),
                                             2: list.copy(self.PLAYER_DATA_FIELDS),
                                             3: list.copy(self.PLAYER_DATA_FIELDS),
                                             4: list.copy(self.PLAYER_DATA_FIELDS),
                                             5: list.copy(self.PLAYER_DATA_FIELDS),
                                             6: list.copy(self.PLAYER_DATA_FIELDS),
                                             7: list.copy(self.PLAYER_DATA_FIELDS),
                                             8: list.copy(self.PLAYER_DATA_FIELDS),
                                             }
                                 }
        self.clear_cards_on_table_and_pot()

    #################################################################################
    # Whenever someone outside (Clients, Server) needs to modify game data.         #
    #    get_thread_safe_comm_packet()                                              #
    #    * do stuff with packet *                                                   #
    #    unlock_thread_safe_comm_packet()                                       #
    #################################################################################

    def get_thread_safe_comm_packet(self):
        locker = QMutexLocker(self.mutex)

        rtrn = GAME_DATA_IN_USE
        if self.mutex.tryLock():
            rtrn = dict.copy(self.GAME_DATA_PACKET)
        else:
            pass
            print(f'get_thread_safe_comm_packet -> GAME_DATA_PACKET is MUTEX Locked.')
        return rtrn

    def unlock_thread_safe_comm_packet(self):
        self.mutex.unlock()

    def set_thread_safe_game_data(self, update):
        if self.mutex.tryLock():
            self.GAME_DATA_PACKET = update
            self.mutex.unlock()
            return True
        else:
            return False

    #################################################################################
    # Dealer Logic                                                                  #
    #################################################################################

    def new_poker_round(self):
        self.deck = self.shuffle_deck()
        self.print_shuffled_deck(self.deck)
        while True:  # try to access the GAME_DATA_PACKET
            if self.mutex.tryLock():  # if access is successful
                self.clear_cards_on_table_and_pot()
                for card_index in range(NUMBER_OF_CARDS_IN_HAND):
                    for player in range(MAX_CLIENTS):
                        if self.GAME_DATA_PACKET["Players"][PACKET_status] is STATUS_PLAYING:
                            self.GAME_DATA_PACKET["Players"][player][PACKET_player_cards][card_index] = self.get_top_card()
                self.mutex.unlock()
                break

    def clear_cards_on_table_and_pot(self):
        self.GAME_DATA_PACKET["Dealer"]["TableCards"] = [NO_CARD, NO_CARD, NO_CARD, NO_CARD, NO_CARD]
        self.GAME_DATA_PACKET["Dealer"]["TablePot"] = 0.0
        for player in range(1, MAX_CLIENTS):
            self.GAME_DATA_PACKET["Players"][player][PACKET_player_cards] = [NO_CARD, NO_CARD]

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
        self.GAME_DATA_PACKET["BurnedCards"] += 1

    def get_top_card(self):
        topCard = self.deck[CARD_INDEX_TOP_CARD]
        self.deck = np.delete(self.deck, CARD_INDEX_TOP_CARD)
        return topCard

    def add_money_to_pot(self, ammount):
        while True:
            if self.mutex.tryLock():  # if GAME_DATA_PACKET is successfully locked from other thread access
                self.GAME_DATA_PACKET["Dealer"]["TablePot"] += float(ammount)
                self.mutex.unlock()
                break

    def add_card_on_table(self, card_number_on_table, card_index_from_deck):
        while True:
            if self.mutex.tryLock():  # if GAME_DATA_PACKET is successfully locked from other thread access
                self.GAME_DATA_PACKET["Dealer"]["TableCards"][card_number_on_table] = card_index_from_deck
                self.mutex.unlock()
                break

    def evaluate_hands(self):
        #TODO: victor leaga magia :)
        pass

