from TeamPokerMainApp.Common.VariableDefinitions import *

GAME_DATA_PACKET = {"Dealer": {"TableCards": [NO_CARD, NO_CARD, NO_CARD, NO_CARD, NO_CARD],
                                            "BurnedCards": int(0),
                                            "TablePot": float(0.0)},
                                 "Players": {1: (int(0), STATUS_EMPTY_SEAT, str(""), int(0), int(0), float(0.0), str(""), [NO_CARD, NO_CARD]),
                                             2: (int(0), STATUS_EMPTY_SEAT, str(""), int(0), int(0), float(0.0), str(""), [NO_CARD, NO_CARD]),
                                             3: (int(0), STATUS_EMPTY_SEAT, str(""), int(0), int(0), float(0.0), str(""), [NO_CARD, NO_CARD]),
                                             4: (int(0), STATUS_EMPTY_SEAT, str(""), int(0), int(0), float(0.0), str(""), [NO_CARD, NO_CARD]),
                                             5: (int(0), STATUS_EMPTY_SEAT, str(""), int(0), int(0), float(0.0), str(""), [NO_CARD, NO_CARD]),
                                             6: (int(0), STATUS_EMPTY_SEAT, str(""), int(0), int(0), float(0.0), str(""), [NO_CARD, NO_CARD]),
                                             7: (int(0), STATUS_EMPTY_SEAT, str(""), int(0), int(0), float(0.0), str(""), [NO_CARD, NO_CARD]),
                                             8: (int(0), STATUS_EMPTY_SEAT, str(""), int(0), int(0), float(0.0), str(""), [NO_CARD, NO_CARD]),
                                             }
                                 }

testStr = str(GAME_DATA_PACKET)
print(testStr)

backToDict = eval(testStr)
print(backToDict)

print(backToDict == GAME_DATA_PACKET)
