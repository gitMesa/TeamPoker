from TeamPokerMainApp.Common.VariableDefinitions import *
from PyQt5.Qt import QMutex

class NetworkPacket:

    def __init__(self):

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

    def get_copy_of_game_data(self):
        pass