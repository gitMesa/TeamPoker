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
{background: qradialgradient(spread:pad, cx:0.5, cy:0.5, radius:0.584, fx:0.5, fy:0.5, stop:0 rgba(35, 122, 87, 255), stop:1 rgba(9, 48, 40, 255));}
QWidget#widget_current_user
{background: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:0, stop:0 rgba(96, 108, 136, 255), stop:1 rgba(63, 76, 107, 255));}

QWidget#pageMain,
QWidget#pageJoinGame,
QWidget#pageHostGame
{background: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:1, stop:0 rgba(51, 51, 51, 255), stop:1 rgba(221, 24, 24, 255));}

QLabel{color: white;}
QCheckBox{color:white;}
QRadioButton{color:white;}
QGroupBox{color:white;}

/* QPushButton{border: 0px; color: white;} */

QPushButton#buttonHostAGame,
QPushButton#buttonJoinAGame,
QPushButton#buttonStartHostingAGame,
QPushButton#button_host_to_main_page,
QPushButton#buttonStartJoiningAGame,
QPushButton#button_client_to_main_page /*,
QPushButton#button_serverStartGame,
QPushButton#button_serverPauseGame,
QPushButton#button_serverEndGame,
QPushButton#action_call,
QPushButton#action_fold,
QPushButton#action_raise,
QPushButton#action_buy_in,
QPushButton#action_sit_out*/
{border-style: outset;
border-width: 2px;
border-radius: 5px;
border-color: white;
color: white;}

QPushButton#buttonHostAGame:hover,
QPushButton#buttonJoinAGame:hover,
QPushButton#buttonStartHostingAGame:hover,
QPushButton#button_host_to_main_page:hover,
QPushButton#buttonStartJoiningAGame:hover,
QPushButton#button_client_to_main_page:hover /*,
QPushButton#button_serverStartGame:hover,
QPushButton#button_serverPauseGame:hover,
QPushButton#button_serverEndGame:hover,
QPushButton#action_call:hover,
QPushButton#action_fold:hover,
QPushButton#action_raise:hover,
QPushButton#action_buy_in:hover,
QPushButton#action_sit_out:hover */
{border-style: outset;
border-width: 2px;
border-radius: 5px;
border-color: #2193b0;
color: #2193b0;}

/*QPushButton#action_call:checked,
QPushButton#action_fold:checked,
QPushButton#action_raise:checked,
QPushButton#action_buy_in:checked,
QPushButton#action_sit_out:checked
{font-weight: bold;
border-style: outset;
border-width: 2px;
border-radius: 5px;
border-color: #2193b0;
color: #2193b0;}*/

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

QPushButton#cards_tableCard0,
QPushButton#cards_tableCard1,
QPushButton#cards_tableCard2,
QPushButton#cards_tableCard3,
QPushButton#cards_tableCard4,
QPushButton#cards_burnedCards,
QPushButton#icon_potSize
{
border: 0px;
padding: 0px;
margin: 0px;
}

QComboBox#combobox_blind_raise_interval{
    background: transparent;
    border-style: solid;
    border-width: 1px;
    border-color: transparent;
    color: white;}
    
QComboBox#combobox_blind_raise_interval::drop-down{image: url(:/ui_icons/ui_icons/icon_expand.png); subcontrol-position: right;}

QComboBox#combobox_blind_raise_interval QAbstractItemView
{background: qlineargradient(spread:pad, x1:1, y1:0, x2:0, y2:1, stop:0 rgba(51, 51, 51, 255), stop:1 rgba(221, 24, 24, 255)); color: white;}

QComboBox#combobox_blind_raise_interval{
    background: transparent;
    border-style: solid;
    border-width: 1px;
    border-color: transparent;
    color: white;}


QComboBox#combobox_icon_selection{
    background: transparent;
    border-style: solid;
    border-width: 1px;
    border-color: transparent;}

QComboBox#combobox_icon_selection QListView{background: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgba(15, 32, 39, 255), stop:0.5 rgba(32, 58, 67, 255), stop:1 rgba(44, 83, 100, 255));}
QComboBox#combobox_icon_selection QListView::item:hover{background: #2C5364;}
QComboBox#combobox_icon_selection QAbstractItemView {border: 0px; border-color: transparent;}

QComboBox#combobox_icon_selection::drop-down{
   image: url(:/ui_icons/ui_icons/icon_expand.png);
   subcontrol-position: right;}

QComboBox#combobox_icon_selection QScrollBar:vertical{
   border: 1px solid black;
   background: white;
   width: 10px;
   margin: 0px 0px 0px 0px;}

QComboBox#combobox_icon_selection QScrollBar::handle:vertical{
   background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(218, 68, 83, 255), stop:1 rgba(137, 33, 107, 255));
   min-height: 0px;}

QComboBox#combobox_icon_selection QScrollBar::add-line:vertical{
   background: white;
   height: 0px;
   subcontrol-position: bottom;
   subcontrol-origin: margin;}

QComboBox#combobox_icon_selection QScrollBar::sub-line:vertical{
   background: white;
   height: 0px;
   subcontrol-position: top;
   subcontrol-origin: margin;}


"""

