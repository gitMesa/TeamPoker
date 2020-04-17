#################################################################################################
# Various Style Sheets Used
#################################################################################################

WINDOW_STYLE = """
/*
Dark primary color:     #000051
Dark primary color 2:   #001970   < for the panel selection buttons on the left part
Primary color:          #1a237e
Light primary color:    #534bae

Unselected text color: #5d99c6
*/

QWidget#gamePlayPage
{
background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.5, fx:0.5, fy:0.5, stop:0 rgba(57, 90, 58, 255), stop:0.35 rgba(71, 113, 72, 255), stop:1 rgba(89, 141, 90, 255));
}

QLabel{color: white;}


/* Hide Icons */
QPushButton#player0_icon,
QPushButton#player1_icon,
QPushButton#player2_icon,
QPushButton#player3_icon,
QPushButton#player4_icon,
QPushButton#player5_icon,
QPushButton#player6_icon,
QPushButton#player7_icon,

QPushButton#player0_dealer,
QPushButton#player1_dealer,
QPushButton#player2_dealer,
QPushButton#player3_dealer,
QPushButton#player4_dealer,
QPushButton#player5_dealer,
QPushButton#player6_dealer,
QPushButton#player7_dealer,

QPushButton#player0_card1,
QPushButton#player0_card2,
QPushButton#player1_card1,
QPushButton#player1_card2,
QPushButton#player2_card1,
QPushButton#player2_card2,
QPushButton#player3_card1,
QPushButton#player3_card2,
QPushButton#player4_card1,
QPushButton#player4_card2,
QPushButton#player5_card1,
QPushButton#player5_card2,
QPushButton#player6_card1,
QPushButton#player6_card2,
QPushButton#player7_card1,
QPushButton#player7_card2,

QPushButton#cards_tableCard1,
QPushButton#cards_tableCard2,
QPushButton#cards_tableCard3,
QPushButton#cards_tableCard4,
QPushButton#cards_tableCard5,
QPushButton#cards_burnedCards,
QPushButton#icon_potSize
{
border: 0px;
padding: 0px;
margin: 0px;
}

"""

