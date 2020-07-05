from typing import List, Optional

from models.player import Player
from models.suit import Suit


class Round(object):

    players: List[Player]
    bidder_index: int
    trump_suit: Optional[Suit]

    def __init__(self, players: List[Player], bidder_index: int, trump_suit: Suit = None):
        """
        Initializes a Round (i.e. a sequence of 8 tricks).
        :param players: The players present in this round. The order of the players is the order in which
            cards must be played in the 8 tricks that compose this Round. Note that the first trick need
            not be played by the player at index 0; the bidder_index parameter controls this.
        :param bidder_index: The index of the bidding player, i.e. the player that decides the trump suit
            and leads the first trick.
        :param trump_suit: Set the trump suit for this round. Typically, we do not know the trump suit yet
            on initialization, since the bidding player has yet to pick a suit. Hence, it is an optional argument.
        """

        assert len(players) == 4
        assert 0 <= bidder_index < 4
        assert trump_suit is None or isinstance(trump_suit, Suit)
        self.players = players
        self.bidder_index = bidder_index
        self.trump_suit = trump_suit
