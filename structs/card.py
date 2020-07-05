from typing import NamedTuple

from structs.rank import Rank
from structs.suit import Suit


class Card(NamedTuple):
    suit: Suit
    rank: Rank

