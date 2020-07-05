import random
from enum import Enum
from typing import NamedTuple, List, Optional, Set


class Rank(Enum):
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14


class Suit(Enum):
    CLUBS = 1
    HEARTS = 2
    DIAMONDS = 3
    SPADES = 4

    @staticmethod
    def suits():
        return {
            "C": Suit.CLUBS,
            "H": Suit.HEARTS,
            "D": Suit.DIAMONDS,
            "S": Suit.SPADES,
        }


class Card(NamedTuple):
    suit: Suit
    rank: Rank


class Player(object):
    hand: Set[Card]
    name: str

    def __init__(self, hand: Set[Card] = None, name: str = None):
        """
        Initialize a player.

        :param hand: The hand of the player. If left unspecified, an empty hand is assumed.
        :param name: The given name of the player. If left unspecified, a random name is generated.
        """

        self.hand = hand if hand is not None else set()
        self.name = name if name is not None else self.generate_name()

    @staticmethod
    def generate_name() -> str:
        """Generates a random, pronouncable name for a player.

        :return: A random name.
        """

        vowels = ["a", "e", "o"] * 2 + ["i", "u"]
        consonants = ["b", "d", "f", "g", "h", "k", "l", "m", "n", "p", "qu", "r", "s", "t", "v", "y"]

        suffices = ["d", "h", "l", "n", "s"]

        # The core of the name is a randoma mount of consonant+vowel combinations.
        syllables = random.randint(2, 3)
        name = "".join([random.choice(consonants) + random.choice(vowels) for syllable in range(syllables)])

        # Add a prefix in the form of an extra vowel with a certain chance
        if random.randint(0, 1):
            name = random.choice(vowels) + name

        # Add a suffix in the form of a special extra consonant with a certain chance
        if random.randint(0, 1):
            name += random.choice(suffices)

        # Make the first letter uppercase
        name = name.title()

        return name


class Deck(object):
    seed: int = None

    def __init__(self, cards: List[Card] = None):
        """
        Initializes a deck. The cards in it are in the order that it is given.
        To randomize the order of the deck, call `shuffle`.

        :param cards: The cards that the deck holds. If this parameter is not specified,
        a full piquet deck (7-A of all four suits) is used by default.
        """

        # Default the card collection to a full deck if none are specified.
        self.cards = [Card(suit=suit, rank=rank) for suit in Suit for rank in Rank] if cards is None else cards

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

        hand_size = int(len(self.cards) / len(players))

        for player in players:
            player.hand = player.hand.union(set(self.cards[0:hand_size]))
            self.cards = self.cards[hand_size:]

    def __repr__(self):
        return repr(self.cards)

    def __eq__(self, other):
        # In case different seeds result in the same card order,
        # we should of course consider the decks equal anyway.
        return self.cards == other.cards


class Game(object):
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

    def initialize(self) -> None:
        """
        Begins the Round. If no trump suit was yet selected, this will prompt to the bidder to select a suit.
        Input is then redirected to the bidding player to play a card.
        """

        if self.trump_suit is None:
            user_input = input("Select trump suit (H, D, C, S): ")
            self.trump_suit = Suit.suits()[user_input]


class Trick(object):
    """
    A Trick object represents the state of a single trick within a Round.
    A Round essentially contains 8 tricks in total.
    """

    players: List[Player]
    leading_player_index: int

    played_cards: List[Optional[Card]]

    def __init__(self, players: List[Player], leading_player_index: int):
        assert len(players) == 4
        assert 0 <= leading_player_index < 4

        self.players = players
        self.leading_player_index = leading_player_index

        """
        We initialize the played cards to None so that we can avoid KeyErrors,
        as well as assign played cards according to the same indices as the player list.
        This way we can be sure that even if the trick starts with the third player, we
        do not need a dictionary (or similar construct) to map the played cards to the players.
        """
        self.played_cards = [None, None, None, None]

    @property
    def led_suit(self) -> Suit:
        """
        Get the suit with which this trick was led. Equal to the first card played in this trick.
        Returns None if no card has been played yet in this trick.

        :return: Suit
        """
        return (None
                if self.played_cards[self.leading_player_index] is None
                else self.played_cards[self.leading_player_index].suit
                )

    @property
    def player_index_to_play(self) -> int:
        """
        Get the player index whose turn it is to play at the moment. We determine
        this index by observing which player started this trick, and how
        many cards have already been played this trick.

        For return value `idx`, call `self.players[idx]` to get the player him- or herself.

        :return: int
        """

        return self.leading_player_index + len([card for card in self.played_cards if card is not None]) % 4

    @property
    def legal_cards(self) -> Set[Card]:
        """
        Get the cards that can be played legally by the current player.
        TODO: Logic around trump cards is not yet implemented!

        :return: The set of legal cards that can be played.
        """
        hand = self.players[self.player_index_to_play].hand

        if self.led_suit:
            # If the suit has already been decided, the player must follow if possible.
            follow_suit_cards = {card for card in hand if card.suit == self.led_suit}

            # If the player can follow suit, those cards are the only legal ones.
            # Otherwise, the whole hand is legal.
            return follow_suit_cards if follow_suit_cards else hand

        # When leading, any card in hand is legal.
        return hand

    def play(self, card: Card):
        """Play a card to this trick."""

        # If the current player already played a card, he may not play another.
        assert self.played_cards[self.player_index_to_play] is None

        # The card must be legal to play
        assert card in self.legal_cards

        # Remove the card from the player's hand.
        self.players[self.player_index_to_play].hand.remove(card)

        # Add the card to the trick.
        self.played_cards[self.player_index_to_play] = card
