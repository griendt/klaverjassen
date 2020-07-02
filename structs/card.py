from typing import NamedTuple, List
from enum import Enum
import random


class Suit(Enum):
    CLUBS = 1
    HEARTS = 2
    DIAMONDS = 3
    SPADES = 4


class Rank(Enum):
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class Card(NamedTuple):
    suit: Suit
    rank: Rank


class CardCollection(object):
    cards: List[Card]

    def __init__(self, cards: List[Card]):
        self.cards = cards

    def __eq__(self, other):
        return set(self.cards) == set(other.cards)

class Deck(CardCollection):
    seed: int = None

    def __repr__(self):
        return repr(self.cards)

    def __init__(self, cards: CardCollection = None):
        if cards is None:
            self.cards = [
                Card(suit=suit, rank=rank)
                for suit in Suit
                for rank in Rank
            ]
        else:
            self.cards = cards

    def __eq__(self, other):
        # In case different seeds result in the same card order,
        # we should of course consider the decks equal anyway.
        return self.cards == other.cards

