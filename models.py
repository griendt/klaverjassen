import random
from enum import Enum
from typing import NamedTuple, List, Optional, Set, Dict


class Rank(Enum):
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    @staticmethod
    def order():
        """
        The order of the ranks in which cards of the same suit are considered in tricks.
        For the order in the trump suit, see `order_trump`.

        :return: A dictionary keyed by this enum's values mapped to integers.
            Higher integer means higher priority.
        """
        return {
            Rank.SEVEN: 0,
            Rank.EIGHT: 1,
            Rank.NINE: 2,
            Rank.JACK: 3,
            Rank.QUEEN: 4,
            Rank.KING: 5,
            Rank.TEN: 6,
            Rank.ACE: 7,
        }

    @staticmethod
    def order_trump():
        """
        The order of the ranks in which cards of the same suit are considered in tricks,
        given that the suit is the trump suit. For the normal order, see `order`.

        :return: A dictionary keyed by this enum's values mapped to integers.
            Higher integer means higher priority.
        """
        return {
            Rank.SEVEN: 0,
            Rank.EIGHT: 1,
            Rank.QUEEN: 2,
            Rank.KING: 3,
            Rank.TEN: 4,
            Rank.ACE: 5,
            Rank.NINE: 6,
            Rank.JACK: 7
        }


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

    leading_player_index: int
    game: Game
    played_cards: List[Optional[Card]]

    def __init__(self, game: Game, leading_player_index: int):
        assert 0 <= leading_player_index < 4

        self.game = game
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
        TODO: Being forced to play trump is not yet implemented!
        TODO: Not being forced to play trump when the partner has the winning card is not yet implemented!

        :return: The set of legal cards that can be played.
        """
        hand = self.game.players[self.player_index_to_play].hand

        # When leading, any card in hand is legal.
        if not self.led_suit:
            return hand

        # If the suit has already been decided, the player must follow if possible.
        follow_suit_cards = {card for card in hand if card.suit == self.led_suit}

        # If the led suit is the trump suit, only higher trumps are allowed (if available).
        if self.game.trump_suit == self.led_suit:
            higher_trumps_available = {
                card
                for card in follow_suit_cards
                if self.compare_cards(card, self.winning_card) == -1
            }

            if higher_trumps_available:
                # The player has higher trumps than the currently winning trump.
                # Only these cards are legal to play.
                return higher_trumps_available

            # The player has no higher trumps. Go back to the normal routine.

        # If the player can follow suit, those cards are the only legal ones.
        # Otherwise, the whole hand is legal.
        return follow_suit_cards if follow_suit_cards else hand

    @property
    def winning_card_index(self) -> Optional[int]:
        """
        Find the index of the card that ranks the highest in this trick.

        Note that the trick need not yet be complete (4 cards), but at least
        one card needs to be played for this method to make sense.

        :return: The index for `self.played_cards` that is the highest ranked.
            If no card was yet played, returns None.
        """

        winning_index: Optional[int] = None
        for index, card in enumerate(self.played_cards):
            if winning_index is None or (
                card is not None and self.compare_cards(self.played_cards[winning_index], card) == 1
            ):
                winning_index = index

        return winning_index

    @property
    def winning_card(self) -> Card:
        """
        Returns the card that is currently winning the trick.

        Note that the trick need not yet be complete (4 cards), but at least
        one card needs to be played for this method to make sense.

        :return: The winning card. Returns None if no card was yet played.
        """
        return None if self.winning_card_index is None else self.played_cards[self.winning_card_index]

    def compare_cards(self, card_1: Card, card_2: Card) -> int:
        """
        Compare two cards and detect which is considered to rank higher. The highest card
        is considered to win the trick (upon termination of the trick). Note that this is
        a property inherent to a trick, as the led suit and the trump suit must be considered.

        Note that this is unrelated to a card's score!

        :param card_1: The first card.
        :param card_2: The second card.
        :return: A comparison value:
            -1 if the first card is better;
            1 if the second card is better;
            0 if the cards are considered equal.
        """
        if card_1.suit == card_2.suit:
            # The cards are in the same suit. Comparison will be simple: check whether we're
            # dealing with the trump suit, and see which card is higher.
            # Note: if the suit is neither trump not the led suit, the cards are incomparable.

            if card_1.suit == self.game.trump_suit:
                return -1 + 2 * int(Rank.order_trump()[card_1.rank] < Rank.order_trump()[card_2.rank])
            elif self.led_suit is not None and card_1.suit != self.led_suit:
                # The cards are both in a non-trump suit that was also not led.
                # This renders the cards effectively incomparable.
                return 0

            # The cards are in non-trump suit, but are either in the led suit,
            # or no led suit was yet specified. We can compare them in the normal way.
            # This is useful both for determine which card would win given the currently led suit,
            # or to determine which card is better for the current player to lead a fresh trick with.
            return -1 + 2 * int(Rank.order()[card_1.rank] < Rank.order()[card_2.rank])

        # If one of the cards is trump but the other is not, the one card always wins,
        # regardless of the suit that was to be followed.
        if card_1.suit == self.game.trump_suit:
            return -1
        if card_2.suit == self.game.trump_suit:
            return 1

        # Neither card is a trump card; check if either card follows suit. If one does,
        # then that card wins. Otherwise, both cards are irrelevant to the trick and thus equal.
        # Note that if no card has been led yet, these checks will evaluate to false as well.
        if card_1.suit == self.led_suit:
            return -1
        if card_2.suit == self.led_suit:
            return 1

        # The cards differ in suits, neither suit is trump, and neither suit was led.
        # The cards are effectively incomparable.
        return 0

    def play(self, card: Card) -> None:
        """Play a card to this trick."""

        # If the current player already played a card, he may not play another.
        assert self.played_cards[self.player_index_to_play] is None, f"Player index {self.player_index_to_play} already played a card this trick"

        # The card must be legal to play
        assert card in self.legal_cards, f"Card {card} is not legal to play"

        # Remove the card from the player's hand.
        self.game.players[self.player_index_to_play].hand.remove(card)

        # Add the card to the trick.
        self.played_cards[self.player_index_to_play] = card
