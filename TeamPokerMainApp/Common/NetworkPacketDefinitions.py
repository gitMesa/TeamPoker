
# Placeholder definitions to separate player keys from other values.
PL0 = 0
PL1 = 1
PL2 = 2
PL3 = 3
PL4 = 4
PL5 = 5
PL6 = 6
PL7 = 7

# Dealer Field Names
DL_GameName = 10  # Game Name
DL_textTableCenter = 11  # String that will contain the text line that is displayed to players in the center of the table
DL_isGamePlaying = 12  # Contains the state of the game (Playing, Paused, Ended).
DL_Currency = 13  # 3 letter string describing the currency used RON, EUR, USD, etc.
DL_BigBlind = 14  # Value of the Big Blind
DL_TablePot = 15  # Value of the Table Pot
DL_MinBet = 16  # Value of the minimum bet (in case someone raised for example)
DL_idNextDecision = 17  # ID of the player who needs to take a decision next
DL_noBurnedCards = 18  # Number of Burned Cards
DL_TableCards = 19  # Array of Table Cards

# PlayerClient Field Names - start from 20 to differentiate enough from DL fields
PC_Name = 41  # Name of the player
PC_Icon = 42  # String of the icon the player uses TODO: change into ids to make it easier to transmit over network
PC_TableSpot = 43  # The selected spot at the table
PC_BuyInReq = 44  # Request to buy in this amount (to be added at the appropriate time.)
PC_isPlayerPlaying = 45  # True = Playing | False = Sitting Out
PC_idPlayerAction = 46  # Action that this player selected.
PC_BetAmount = 47  # Amount that the player has bet.
PC_ClientOverwrite = 48  # Overwrite param for Client0 to start/pause/end the game forcefully.

# PlayerServer Field Names - start from 40 to differentiate enough from PC fields
PS_ConnectionStatus = 61  # Connection Status of this player.
PS_isDealer = 62  # if the player is dealer
PS_isBlind = 63  # if the player is blind, and is he small/blind
PS_textPlayerTable = 64  # Text that will be displayed besides each player on the table
PS_MoneyBoughtIn = 65  # Value of the total money this player bought in this game
PS_MoneyAvailable = 66  # Value of the money this player has available
PS_PlayerCards = 67  # Array of cards this player has.
