from TeamPokerMainApp.PokerGame.GameUI.UiCode.TeamPokerUI import *


class TeamPokerUIControllerClass(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(TeamPokerUIControllerClass, self).__init__(parent)
        self.setupUi(self)

    def showMainWindow(self):
        self.show()
