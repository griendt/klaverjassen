from typing import List

from models.player import Player


class Round(object):

    players: List[Player]
    bidder_index: int

    def __init__(self, players: List[Player], bidder_index: int):
        """
        Initializes a Round (i.e. a sequence of 8 tricks).
        :param players: The players present in this round. The order of the players is the order in which
            cards must be played in the 8 tricks that compose this Round. Note that the first trick need
            not be played by the player at index 0; the bidder_index parameter controls this.
        :param bidder_index: The index of the bidding player, i.e. the player that decides the trump suit
            and leads the first trick.
        """

        assert len(players) == 4
        assert 0 <= bidder_index < 4
        self.players = players
        self.bidder_index = bidder_index
