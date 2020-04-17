################################
#   Other Random Definitions   #
################################
NUMBER_INDEX_TUPLE = 0
COLOR_INDEX_TUPLE = 1
NO_CARD = 99

# Table Status
STATUS_T_EMPTY_SEAT = 0
STATUS_T_CONNECTED = 1
STATUS_T_DISCONNECTED = 2
STATUS_T_CONNECTION_LOST = 3
STATUS_T_SIT_OUT_TURN = 4

# Game Status
STATUS_G_PLAYING = 5
STATUS_G_DEALER = 6
STATUS_G_SMALL_BLIND = 7
STATUS_G_BIG_BLIND = 8
STATUS_G_NONE = 9

# Dealer Status
STATUS_D_WAITING_FOR_PLAYERS = 10
STATUS_D_GAME_STATUS_NEW_ROUND_READY = 11
STATUS_D_GAME_STATUS_PLAYER_DECIDING = 12
STATUS_D_GAME_STATUS_EVALUATE_HANDS = 13

################################
#    Server/Client Stuff Def   #
################################

DEALER = 0
MAX_CLIENTS = 8  # Host(Dealer+Client) + 7 other players = 8 total players
MESSAGE_DISCONNECTED = '!DISCONNECTED'
BUFFERSIZE = 2048
FORMAT = 'utf-8'

# Player field decided by the Player
PINFO_tableSpot = 0
PINFO_status = 1
PINFO_name = 2
PINFO_icon = 3
PINFO_actionID = 4

# Player fields decided by the Dealer
PGAME_moneyAvailable = 0
PGAME_dealerStatus = 1
PGAME_dealerIcon = 2
PGAME_blindStatus = 3
PGAME_blindIcon = 4
PGAME_playerCards = 5

ACTION_FOLD = 0
ACTION_CALL = 1
ACTION_RAISE = 2
ACTION_SIT_OUT = 3

################################
#    Deck Stuff Definitions    #
################################
NUMBER_OF_CARDS_IN_DECK = 52
NUMBER_OF_CARDS_IN_HAND = 2
NUMBER_OF_CARDS_ON_TABLE = 5
NUMBER_OF_CARDS_ON_FLOP = 3
NUMBER_OF_CARDS_ON_TURN = 1
NUMBER_OF_CARDS_ON_RIVER = 1
NUMBER_OF_CARDS_TO_EVALUATE = 7
NUMBER_OF_CARDS_FOR_WIN = 5

A_NUMBER = 14
K_NUMBER = 13
Q_NUMBER = 12
J_NUMBER = 11

CARD_SIGNS = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K', 'A']
CARD_SIGNS_INDEX = [2, 3, 4, 5, 6, 7, 8, 9, 10, J_NUMBER, Q_NUMBER, K_NUMBER, A_NUMBER]
#CARD_SUITS = ['♡', '♤', '♧', '♢']
CARD_SUITS = ['H', 'S', 'C', 'D']
CARD_SUITS_TEXT = ['heart', 'spade', 'club', 'diamond']

CARD_INDEX_TURN = 3
CARD_INDEX_RIVER = 4
CARD_INDEX_TOP_CARD = 0

#####################################
#    Hand Evaluation Definitions    #
#####################################

SMALL_STRAIGHT = [2, 3, 4, 5, 14]
NUMBER_OF_CARDS_FOR_QUADS = 4
NUMBER_OF_CARDS_FOR_TRIPS = 3

ROYAL_FLUSH_RANK = 1
STRAIGHT_FLUSH_RANK = 2
QUADS_RANK = 3
FULL_HOUSE_RANK = 4
FLUSH_RANK = 5
STRAIGHT_RANK = 6
TRIPS_RANK = 7
TWO_PAIRS_RANK = 8
PAIR_RANK = 9
HIGH_CARD_RANK = 10

ROYAL_FLUSH_DESCRIPTION = "royal flush"
STRAIGHT_FLUSH_DESCRIPTION = "straight flush"
QUADS_DESCRIPTION = "quads"
FULL_HOUSE_DESCRIPTION = "full house"
FLUSH_DESCRIPTION = "flush"
STRAIGHT_DESCRIPTION = "straight"
TRIPS_DESCRIPTION = "trips"
TWO_PAIRS_DESCRIPTION = "two pair"
PAIR_DESCRIPTION = "pair"
HIGH_CARD_DESCRIPTION = "high card"
