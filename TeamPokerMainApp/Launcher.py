from TeamPokerMainApp.PokerGame.PokerGame import PokerGameClass
from PyQt5.QtWidgets import QApplication
import sys


class TeamPokerMain:

    def __init__(self):
        self._poker = PokerGameClass()
        self._poker.show_main_window()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TeamPokerMain()
    app.exec()
