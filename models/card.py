from typing import NamedTuple

from models.rank import Rank
from models.suit import Suit


class Card(NamedTuple):
    suit: Suit
    rank: Rank
