import random
from typing import List

from structs.card import Suit, Rank, Card
from structs.cardCollection import CardCollection
from structs.player import Player


class Deck(CardCollection):
    seed: int = None

    def __init__(self, cards: CardCollection = None):
        """
        Initializes a deck. The cards in it are in the order that it is given.
        To randomize the order of the deck, call `shuffle`.

        :param cards: The cards that the deck holds. If this parameter is not specified,
        a full piquet deck (7-A of all four suits) is used by default.
        """

        # Default the card collection to a full deck if none are specified.
        cards = [
            Card(suit=suit, rank=rank)
            for suit in Suit
            for rank in Rank
        ] if cards is None else cards
        super().__init__(cards)

    def shuffle(self, seed: int = None) -> None:
        """
        Shuffle the deck's cards according to the seed.
        If no seed is given, a random seed is used.

        :param seed: The seed to use for the RNG.
        """
        rng = random.Random()
        self.seed = seed if seed is not None else rng.randint(0, 100000000)
        rng.seed(self.seed)
        rng.shuffle(self.cards)

    def deal(self, players: List[Player]) -> None:
        """
        Deal the deck among the players.

        :param players: The list of players. The cards are dealt in the order in which the players are given.
        """
        if len(self.cards) % len(players) != 0:
            raise ValueError(f"Cannot evenly deal {len(self.cards)} cards among {len(players)} players")

        hand_size = int(len(self.cards)/len(players))

        for player in players:
            player.hand += self.cards[0:hand_size]
            self.cards = self.cards[hand_size:]

    def __repr__(self):
        return repr(self.cards)

    def __eq__(self, other):
        # In case different seeds result in the same card order,
        # we should of course consider the decks equal anyway.
        return self.cards == other.cards
