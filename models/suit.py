from enum import Enum


class Suit(Enum):
    CLUBS = 1
    HEARTS = 2
    DIAMONDS = 3
    SPADES = 4


def suits():
    return {
        "C": Suit.CLUBS,
        "H": Suit.HEARTS,
        "D": Suit.DIAMONDS,
        "S": Suit.SPADES,
    }
