from TeamPokerMainApp.Common.VariableDefinitions import *

########################################
#    Communication Packet Definition   #
########################################


class NetworkPacketClass:

    COMM_PACKET_status = 0
    COMM_PACKET_name = 1
    COMM_PACKET_icon_id = 2
    COMM_PACKET_action_id = 3
    COMM_PACKET_money_available = 4
    COMM_PACKET_player_cards = 5

    COMMUNICATION_PACKET = {"TableCards": [NO_CARD, NO_CARD, NO_CARD, NO_CARD, NO_CARD],
                            "BurnedCards": int,
                            "TablePot": float,
                            "Players": {
                                1: (int, str, int, int, float, [NO_CARD, NO_CARD]),
                                2: (int, str, int, int, float, [NO_CARD, NO_CARD]),
                                3: (int, str, int, int, float, [NO_CARD, NO_CARD]),
                                4: (int, str, int, int, float, [NO_CARD, NO_CARD]),
                                5: (int, str, int, int, float, [NO_CARD, NO_CARD]),
                                6: (int, str, int, int, float, [NO_CARD, NO_CARD]),
                                7: (int, str, int, int, float, [NO_CARD, NO_CARD]),
                                8: (int, str, int, int, float, [NO_CARD, NO_CARD]),
                            }
                            }

    def getCommunicationPacket(self):
        return self.COMMUNICATION_PACKET
