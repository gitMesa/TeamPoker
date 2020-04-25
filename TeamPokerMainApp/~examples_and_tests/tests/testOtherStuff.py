from TeamPokerMainApp.Multiplayer.NetworkPacket import *


class Test(NetworkPacketClass):

    def __init__(self):
        self.game_data = self.get_network_packet_definition()

    def find_playing_players_and_setup_dealer_and_first_blinds(self):
        playing_players = []  # Empty list
        for player in range(MAX_CLIENTS):
            if self.game_data["PlayerClient"][player]["PlayerStatus"] is PLAYER_STATUS_player_is_playing:
                # add them to the list of currently playing players
                playing_players.append(player)
            # reset all statuses
            self.game_data["PlayerDealer"][player]["isDealer"] = TABLE_STATUS_is_NORMAL_PLAYER
            self.game_data["PlayerDealer"][player]["isBlind"] = TABLE_STATUS_is_NORMAL_PLAYER

        if len(playing_players) >= 3:
            self.game_data["PlayerDealer"][playing_players[0]]["isDealer"] = TABLE_STATUS_is_DEALER
            self.game_data["PlayerDealer"][playing_players[1]]["isBlind"] = TABLE_STATUS_is_SMALL_BLIND
            self.game_data["PlayerDealer"][playing_players[2]]["isBlind"] = TABLE_STATUS_is_BIG_BLIND
            # Roll the playing_players list until big blind is the last in the list
            self.dealer_roll_playing_players_list(playing_player_array=playing_players, last_player_index=playing_players[2])

        elif len(playing_players) == 2:
            self.game_data["PlayerDealer"][playing_players[0]]["isDealer"] = TABLE_STATUS_is_DEALER
            self.game_data["PlayerDealer"][playing_players[1]]["isBlind"] = TABLE_STATUS_is_SMALL_BLIND
            self.game_data["PlayerDealer"][playing_players[0]]["isBlind"] = TABLE_STATUS_is_BIG_BLIND
            self.dealer_roll_playing_players_list(playing_player_array=playing_players, last_player_index=playing_players[0])

        self.game_data["Dealer"]["NextDecision"] = playing_players[0]
        return playing_players

    def dealer_roll_playing_players_list(self, playing_player_array, last_player_index):
        while playing_player_array[-1] != last_player_index:
            playing_player_array.append(playing_player_array[0])
            playing_player_array.remove(playing_player_array[0])
        return playing_player_array


testing = Test()
testing.game_data["PlayerClient"][0]["PlayerStatus"] = PLAYER_STATUS_player_is_playing
testing.game_data["PlayerClient"][1]["PlayerStatus"] = PLAYER_STATUS_player_is_playing
testing.find_playing_players_and_setup_dealer_and_first_blinds()