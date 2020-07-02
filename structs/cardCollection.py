from typing import List

from structs.card import Card


class CardCollection(object):
    cards: List[Card]

    def __init__(self, cards: List[Card]):
        self.cards = cards

    def __eq__(self, other):
        # The order in which the cards are listed is not relevant for equality.
        # In card collections in which the order is relevant, you should override this method.
        return set(self.cards) == set(other.cards)

    def __len__(self):
        return len(self.cards)

    def __iadd__(self, other):
        if isinstance(other, list):
            self.cards += other
        elif isinstance(other, CardCollection):
            self.cards += other.cards
        else:
            raise TypeError(f"unsupported operand type(s) for +=: 'CardCollection' and '{other.__name__}'")

        return self
