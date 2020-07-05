from typing import List

from models.card import Card


class Players(object):
    pass


class Trick(object):
    """
    A Trick object represents the state of a single trick within a Round.
    A Round essentially contains 8 tricks in total.
    """

    players: List[Players]
    leading_player_index: int

    played_cards: List[Card]

    def __init__(self, players: List[Players], leading_player_index: int):
        assert len(players) == 4
        assert 0 <= leading_player_index < 4

        self.players = players
        self.leading_player_index = leading_player_index

