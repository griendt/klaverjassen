from typing import NamedTuple, List

from structs.rank import Rank
from structs.suit import Suit


class Card(NamedTuple):
    suit: Suit
    rank: Rank


class CardCollection(object):
    cards: List[Card]

    def __init__(self, cards: List[Card]):
        self.cards = cards

    def __eq__(self, other):
        # The order in which the cards are listed is not relevant for equality.
        # In card collections in which the order is relevant, you should override this method.
        return set(self.cards) == set(other.cards)
