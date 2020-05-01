# Dealer Field Names
DL = 0
DL_GameName = 1  # Game Name
DL_textTableCenter = 2  # String that will contain the text line that is displayed to players in the center of the table
DL_isGamePlaying = 3  # Contains the state of the game (Playing, Paused, Ended).
DL_Currency = 4  # 3 letter string describing the currency used RON, EUR, USD, etc.
DL_BigBlind = 5  # Value of the Big Blind
DL_TablePot = 6  # Value of the Table Pot
DL_MinBet = 7  # Value of the minimum bet (in case someone raised for example)
DL_idNextDecision = 8  # ID of the player who needs to take a decision next
DL_noBurnedCards = 9  # Number of Burned Cards
DL_TableCards = 10  # Array of Table Cards

# PlayerClient Field Names - start from 20 to differentiate enough from DL fields
PC = 20
PC_Name = 21  # Name of the player
PC_Icon = 22  # String of the icon the player uses TODO: change into ids to make it easier to transmit over network
PC_TableSpot = 23  # The selected spot at the table
PC_BuyInReq = 24  # Request to buy in this amount (to be added at the appropriate time.)
PC_isPlayerPlaying = 25  # True = Playing | False = Sitting Out
PC_idPlayerAction = 27  # Action that this player selected.
PC_BetAmount = 28  # Amount that the player has bet.
PC_ClientOverwrite = 29  # Overwrite param for Client0 to start/pause/end the game forcefully.

# PlayerServer Field Names - start from 40 to differentiate enough from PC fields
PS = 40
PS_ConnectionStatus = 41  # Connection Status of this player.
PS_isDealer = 42  # if the player is dealer
PS_isBlind = 44  # if the player is blind, and is he small/blind
PS_textPlayerTable = 45  # Text that will be displayed besides each player on the table
PS_MoneyBoughtIn = 46  # Value of the total money this player bought in this game
PS_MoneyAvailable = 47  # Value of the money this player has available
PS_PlayerCards = 48  # Array of cards this player has.
