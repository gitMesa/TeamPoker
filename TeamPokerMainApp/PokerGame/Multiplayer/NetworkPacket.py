from TeamPokerMainApp.Common.VariableDefinitions import *

########################################
#    Communication Packet Definition   #
########################################


class NetworkPacketClass:

    # Defined in VariableDefinitions.py
    # COMM_PACKET_status = 0
    # COMM_PACKET_name = 1
    # COMM_PACKET_icon_id = 2
    # COMM_PACKET_action_id = 3
    # COMM_PACKET_money_available = 4
    # COMM_PACKET_dealer_icon = 5
    # COMM_PACKET_player_cards = 6

    COMMUNICATION_PACKET = {"Dealer": {"TableCards": [NO_CARD, NO_CARD, NO_CARD, NO_CARD, NO_CARD],
                                       "BurnedCards": int,
                                       "TablePot": float
                                       },
                            "Players": {
                                1: (STATUS_EMPTY_SEAT, str, int, int, float, str, [NO_CARD, NO_CARD]),
                                2: (STATUS_EMPTY_SEAT, str, int, int, float, str, [NO_CARD, NO_CARD]),
                                3: (STATUS_EMPTY_SEAT, str, int, int, float, str, [NO_CARD, NO_CARD]),
                                4: (STATUS_EMPTY_SEAT, str, int, int, float, str, [NO_CARD, NO_CARD]),
                                5: (STATUS_EMPTY_SEAT, str, int, int, float, str, [NO_CARD, NO_CARD]),
                                6: (STATUS_EMPTY_SEAT, str, int, int, float, str, [NO_CARD, NO_CARD]),
                                7: (STATUS_EMPTY_SEAT, str, int, int, float, str, [NO_CARD, NO_CARD]),
                                8: (STATUS_EMPTY_SEAT, str, int, int, float, str, [NO_CARD, NO_CARD]),
                            }
                            }

    def getCommunicationPacket(self):
        return self.COMMUNICATION_PACKET
