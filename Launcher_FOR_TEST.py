from TeamPokerMainApp.PokerGame import PokerGameClass
from PyQt5.QtWidgets import QApplication
import sys


class TeamPokerMain:

    def __init__(self):
        self._poker0 = PokerGameClass()
        self._poker0.show_main_window()
        # Start Server
        self._poker0.setDevUserName(username='Server', icon_index=0)
        self._poker0.start_poker_server()
        self._poker0.setDevClickPlayButton()

        # Start Clients
        self._poker1 = PokerGameClass()
        self._poker1.show_main_window()
        self._poker1.setDevUserName(username='test1', icon_index=1)
        self._poker1.join_poker_server()
        self._poker1.setDevClickPlayButton()

        self._poker2 = PokerGameClass()
        self._poker2.show_main_window()
        self._poker2.setDevUserName(username='test2', icon_index=2)
        self._poker2.join_poker_server()
        self._poker2.setDevClickPlayButton()

        self._poker3 = PokerGameClass()
        self._poker3.show_main_window()
        self._poker3.setDevUserName(username='test3', icon_index=3)
        self._poker3.join_poker_server()
        self._poker3.setDevClickPlayButton()

        self._poker4 = PokerGameClass()
        self._poker4.show_main_window()
        self._poker4.setDevUserName(username='test4', icon_index=4)
        self._poker4.join_poker_server()
        self._poker4.setDevClickPlayButton()

        self._poker5 = PokerGameClass()
        self._poker5.show_main_window()
        self._poker5.setDevUserName(username='test5', icon_index=5)
        self._poker5.join_poker_server()
        self._poker5.setDevClickPlayButton()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TeamPokerMain()
    app.exec()
