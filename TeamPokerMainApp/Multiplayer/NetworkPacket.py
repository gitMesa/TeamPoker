from TeamPokerMainApp.Common.VariableDefinitions import *


class NetworkPacketClass:

    @staticmethod
    def get_network_packet_definition():
        # "Dealer" General info fields that describe the various state of the game
        SERVER_DEALER_FIELDS = {DL_GameName: str(""),  # Game Name
                                DL_textTableCenter: str(""),  # String that will contain the text line that is displayed to players in the center of the table
                                DL_isGamePlaying: GAME_is_PAUSED,  # Contains the state of the game (Playing, Paused, Ended).
                                DL_Currency: str(""),  # 3 letter string describing the currency used RON, EUR, USD, etc.
                                DL_BigBlind: float(0.0),
                                DL_TablePot: float(0.0),
                                DL_MinBet: float(0.0),  # Current minimum amount that can be bet (in case someone raised for example)
                                DL_idNextDecision: int(99),  # index for the list of playing players (which itself contains indexes of players)
                                DL_noBurnedCards: int(0),  # Number of Burned Cards
                                DL_TableCards: [NO_CARD, NO_CARD, NO_CARD, NO_CARD, NO_CARD]}

        # "PlayerClient" Fields that are edited by the Player Client and sent to the Server.
        PLAYER_CLIENT_FIELDS = {PC_Name: str(""),
                                PC_Icon: str(""),
                                PC_TableSpot: int(0),
                                PC_BuyInReq: float(0.0),
                                PC_idPlayerAction: ACTION_UNDECIDED,
                                PC_isPlayerPlaying: False,  # True = Playing | False = Sitting Out
                                PC_textPlayerTable: str(""),
                                PC_BetAmount: float(0.0),
                                PC_ClientOverwrite: Overwrite_PAUSE_GAME}

        # "PlayerServer" Fields that are edited by the Server and are sent to the Player Client
        PLAYER_SERVER_FIELDS = {PS_ConnectionStatus: CONN_STATUS_EMPTY_SEAT,
                                PS_isDealer: TABLE_STATUS_is_NORMAL_PLAYER,
                                PS_isBlind: TABLE_STATUS_is_NORMAL_PLAYER,
                                PS_MoneyBoughtIn: float(0.0),
                                PS_MoneyAvailable: float(0.0),
                                PS_PlayerCards: [NO_CARD, NO_CARD]}

        GAME_DATA_PACKET = {DL: SERVER_DEALER_FIELDS,

                            PC: {0: dict.copy(PLAYER_CLIENT_FIELDS),
                                 1: dict.copy(PLAYER_CLIENT_FIELDS),
                                 2: dict.copy(PLAYER_CLIENT_FIELDS),
                                 3: dict.copy(PLAYER_CLIENT_FIELDS),
                                 4: dict.copy(PLAYER_CLIENT_FIELDS),
                                 5: dict.copy(PLAYER_CLIENT_FIELDS),
                                 6: dict.copy(PLAYER_CLIENT_FIELDS),
                                 7: dict.copy(PLAYER_CLIENT_FIELDS)},

                            PS: {0: dict.copy(PLAYER_SERVER_FIELDS),
                                 1: dict.copy(PLAYER_SERVER_FIELDS),
                                 2: dict.copy(PLAYER_SERVER_FIELDS),
                                 3: dict.copy(PLAYER_SERVER_FIELDS),
                                 4: dict.copy(PLAYER_SERVER_FIELDS),
                                 5: dict.copy(PLAYER_SERVER_FIELDS),
                                 6: dict.copy(PLAYER_SERVER_FIELDS),
                                 7: dict.copy(PLAYER_SERVER_FIELDS)}
                            }

        return dict.copy(GAME_DATA_PACKET)
