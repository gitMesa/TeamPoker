# When you don't have cards you don't play... :)
NO_CARD = 99
NO_CARD_IMAGE = '99_red'

# Table Status
CONN_STATUS_EMPTY_SEAT = 0
CONN_STATUS_CONNECTED = 1
CONN_STATUS_DISCONNECTED = 2

GAME_STATUS_PLAYER_PLAYING = 3
GAME_STATUS_PLAYER_SIT_OUT_TURN = 4

TABLE_STATUS_is_DEALER = 5
TABLE_STATUS_is_SMALL_BLIND = 6
TABLE_STATUS_is_BIG_BLIND = 7
TABLE_STATUS_is_NORMAL_PLAYER = 8

ACTION_CALL = 0
ACTION_RAISE = 1
ACTION_FOLD = 2
ACTION_UNDECIDED = 3

# Dealer Status
DEALER_thinks_GAME_is_PLAYING = 10
DEALER_thinks_GAME_is_PAUSED = 11
DEALER_thinks_GAME_is_ENDING = 12

# Dealer Steps
DEALER_WAITING_FOR_GAME_START = 0
DEALER_NEW_GAME = 1
DEALER_WAIT_FOR_PLAYER_ACTION = 2
DEALER_HANDLE_NEXT_ROUND = 3
DEALER_EVALUATE_HANDS_AND_END_GAME = 4

# Poker Rounds
ROUND_PRE_FLOP = 0
ROUND_FLOP = 1
ROUND_TURN = 2
ROUND_RIVER = 3
ROUND_END = 4

# Other Definitions
DEALER = 0
MAX_CLIENTS = 8  # Host(Dealer+Client) + 7 other players = 8 total players
MESSAGE_DISCONNECTED = '!DISCONNECTED'
COMMUNCATION_TIME = 300  # miliseconds
BUFFERSIZE = 10240
HEADER = 64
FORMAT = 'utf-8'

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
NUMBER_INDEX_TUPLE = 0
COLOR_INDEX_TUPLE = 1

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
