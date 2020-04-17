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

QWidget#widget_table
{background: qradialgradient(spread:pad, cx:0.48, cy:0.498, radius:0.458, fx:0.48, fy:0.498, stop:0.111111 rgba(15, 155, 15, 239), stop:0.631258 rgba(6, 23, 0, 246), stop:0.847375 rgba(6, 23, 0, 255));}
QWidget#widget_current_user
{background: qlineargradient(spread:pad, x1:0.477273, y1:0, x2:1, y2:1, stop:0 rgba(35, 7, 77, 255), stop:1 rgba(204, 83, 51, 255));}

QWidget#pageMain,
QWidget#pageJoinGame,
QWidget#pageHostGame
{
background: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:1, stop:0 rgba(51, 51, 51, 255), stop:1 rgba(221, 24, 24, 255))
}

QLabel{color: white;}
QCheckBox{color:white;}
QRadioButton{color:white;}
QGroupBox{color:white;}

QPushButton{border: 0px; color: white;}

QPushButton#buttonHostAGame,
QPushButton#buttonJoinAGame
{border-style: outset;
border-width: 1px;
border-radius: 5px;
border-color: white;
color: white;}

QPushButton#buttonHostAGame:hover,
QPushButton#buttonJoinAGame:hover
{border-style: outset;
border-width: 1px;
border-radius: 5px;
border-color: #2193b0;
color: #2193b0;}

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

