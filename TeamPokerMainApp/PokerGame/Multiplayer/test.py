from TeamPokerMainApp.PokerGame.Multiplayer.Client import ClientModeClass
from TeamPokerMainApp.PokerGame.Multiplayer.Server import ServerModeClass
from _thread import *


class test:

    def __init__(self):
        self._srv = ServerModeClass()
        self._srv.setup_server_networking()
        start_new_thread(self._srv.server_listen_loop(), self)

        self._clt = ClientModeClass()
        self._clt.connect()


app = test()
