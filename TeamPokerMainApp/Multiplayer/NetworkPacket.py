from TeamPokerMainApp.Common.VariableDefinitions import *


class NetworkPacketClass:

    def __init__(self):

        self.PLAYER_FIELDS = {"Name": str(""),
                              "Icon": str(""),
                              "TableSpot": int(0),
                              "ConnectionStatus": CONN_STATUS_EMPTY_SEAT,
                              "GameStatus": GAME_STATUS_PLAYER_SIT_OUT_TURN,
                              "GameAction": ACTION_UNDECIDED,
                              "DealerStatus": TABLE_STATUS_is_NORMAL_PLAYER,
                              "DealerIcon": str(""),
                              "BlindStatus": TABLE_STATUS_is_NORMAL_PLAYER,
                              "BlindIcon": str(""),
                              "BetAmount": float(0.0),
                              "MoneyAvailable": float(0.0),
                              "PlayerCards": [NO_CARD, NO_CARD]}

        self.GAME_DATA_PACKET = {"Dealer": {"GameName": str(""),
                                            "Currency": str(""),
                                            "BigBlind": float(0.0),
                                            "TableCards": [NO_CARD, NO_CARD, NO_CARD, NO_CARD, NO_CARD],
                                            "BetValue": float(0.0),
                                            "BurnedCards": int(0),
                                            "TablePot": float(0.0),
                                            "NextDecision": int(0),
                                            "GameStatus": str('')
                                            },
                                 "Player": {0: dict.copy(self.PLAYER_FIELDS),
                                            1: dict.copy(self.PLAYER_FIELDS),
                                            2: dict.copy(self.PLAYER_FIELDS),
                                            3: dict.copy(self.PLAYER_FIELDS),
                                            4: dict.copy(self.PLAYER_FIELDS),
                                            5: dict.copy(self.PLAYER_FIELDS),
                                            6: dict.copy(self.PLAYER_FIELDS),
                                            7: dict.copy(self.PLAYER_FIELDS),
                                            }
                                 }

    def get_game_data(self):
        return self.GAME_DATA_PACKET
