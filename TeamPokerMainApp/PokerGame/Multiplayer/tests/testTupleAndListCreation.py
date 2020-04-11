from TeamPokerMainApp.Common.VariableDefinitions import *

PLAYER_DATA_FIELDS = (int(0), STATUS_EMPTY_SEAT, str(""), str(""), int(0), float(0.0), str(""), [NO_CARD, NO_CARD])

GAME_DATA_PACKET = {"Dealer": {"TableCards": [NO_CARD, NO_CARD, NO_CARD, NO_CARD, NO_CARD],
                               "BurnedCards": int(0),
                               "TablePot": float(0.0)},
                    "Players": {1: list(PLAYER_DATA_FIELDS),
                                2: list(PLAYER_DATA_FIELDS),
                                3: list(PLAYER_DATA_FIELDS),
                                4: list(PLAYER_DATA_FIELDS),
                                }
                    }

print(type(GAME_DATA_PACKET["Players"][1][PACKET_icon]))
print(type(GAME_DATA_PACKET["Players"][1]))
print(type(GAME_DATA_PACKET["Players"]))
print(type(GAME_DATA_PACKET))

