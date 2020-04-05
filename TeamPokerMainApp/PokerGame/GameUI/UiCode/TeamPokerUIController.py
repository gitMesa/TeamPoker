from TeamPokerMainApp.PokerGame.GameUI.UiCode.TeamPokerUI import *

PAGE_MAIN = 0
PAGE_HOST_A_GAME = 1
PAGE_JOIN_A_GAME = 2
PAGE_PLAYING_ARENA = 3


class TeamPokerUIControllerClass(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(TeamPokerUIControllerClass, self).__init__(parent)
        self.setupUi(self)
        self.stackedWidget.setCurrentIndex(PAGE_MAIN)
        self.buttonHostAGame.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_HOST_A_GAME))
        self.buttonJoinAGame.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_JOIN_A_GAME))
        self.button_test_play_arena.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_PLAYING_ARENA))
        self.button_client_to_main_page.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_MAIN))
        self.button_host_to_main_page.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_MAIN))
        self.button_play_arena_to_main_page.clicked.connect(lambda f: self.stackedWidget.setCurrentIndex(PAGE_MAIN))

    def showMainWindow(self):
        self.show()

    def connectButtonHostGame(self, callback_function):
        self.buttonStartHostingAGame.clicked.connect(callback_function)

    def connectButtonJoinGame(self, callback_function):
        self.buttonJoinAGame.clicked.connect(callback_function)
