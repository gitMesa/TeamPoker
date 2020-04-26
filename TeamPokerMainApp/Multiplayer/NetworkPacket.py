from TeamPokerMainApp.Common.VariableDefinitions import *


class NetworkPacketClass:

    @staticmethod
    def get_network_packet_definition():
        # "Dealer" General info fields that describe the state of the game
        SERVER_DEALER_FIELDS = {"GameName": str(""),
                                "GameStatus": str(""),  # String that will contain the status that is displayed to players in the center of the table
                                "GameState": DEALER_thinks_GAME_is_PAUSED,  # Contains the state of the game (Playing, Paused, Ended).

                                "Currency": str(""),  # 3 letter string describing the currency used RON, EUR, USD, etc.
                                "BigBlind": float(0.0),
                                "TablePot": float(0.0),
                                "MinAllowedBet": float(0.0),  # Current minimum amount that can be bet (in case someone raised for example)

                                "NextDecision": int(99),  # index for the list of playing players (which itself contains indexes of players)

                                "BurnedCards": int(0),
                                "TableCards": [NO_CARD, NO_CARD, NO_CARD, NO_CARD, NO_CARD]}

        # "PlayerClient" Player -> Server communication
        PLAYER_CLIENT_FIELDS = {"Name": str(""),
                                "Icon": str(""),
                                "TableSpot": int(0),
                                "AskForBuyIn": float(0.0),
                                "PlayerAction": ACTION_UNDECIDED,
                                "PlayerStatus": PLAYER_STATUS_player_sit_out_next_turn,
                                "BetAmount": float(0.0),
                                "Client0ServerOverwrite": CLIENT0_FORCE_PAUSE}

        # "PlayerServer" Server -> Player communication
        PLAYER_SERVER_FIELDS = {"ConnectionStatus": CONN_STATUS_EMPTY_SEAT,
                                "isDealer": TABLE_STATUS_is_NORMAL_PLAYER,
                                "DealerIcon": str(""),
                                "isBlind": TABLE_STATUS_is_NORMAL_PLAYER,
                                "BlindIcon": str(""),
                                "MoneyBoughtIn": float(0.0),
                                "MoneyAvailable": float(0.0),
                                "PlayerCards": [NO_CARD, NO_CARD]}

        GAME_DATA_PACKET = {"Dealer": SERVER_DEALER_FIELDS,

                            "PlayerClient": {0: dict.copy(PLAYER_CLIENT_FIELDS),
                                             1: dict.copy(PLAYER_CLIENT_FIELDS),
                                             2: dict.copy(PLAYER_CLIENT_FIELDS),
                                             3: dict.copy(PLAYER_CLIENT_FIELDS),
                                             4: dict.copy(PLAYER_CLIENT_FIELDS),
                                             5: dict.copy(PLAYER_CLIENT_FIELDS),
                                             6: dict.copy(PLAYER_CLIENT_FIELDS),
                                             7: dict.copy(PLAYER_CLIENT_FIELDS)},

                            "PlayerServer": {0: dict.copy(PLAYER_SERVER_FIELDS),
                                             1: dict.copy(PLAYER_SERVER_FIELDS),
                                             2: dict.copy(PLAYER_SERVER_FIELDS),
                                             3: dict.copy(PLAYER_SERVER_FIELDS),
                                             4: dict.copy(PLAYER_SERVER_FIELDS),
                                             5: dict.copy(PLAYER_SERVER_FIELDS),
                                             6: dict.copy(PLAYER_SERVER_FIELDS),
                                             7: dict.copy(PLAYER_SERVER_FIELDS)}
                            }

        return dict.copy(GAME_DATA_PACKET)
