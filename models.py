from __future__ import annotations

import random
from enum import Enum
from typing import NamedTuple, List, Optional, Set, Dict, Any


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
    def order() -> Dict[Rank, int]:
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
    def order_trump() -> Dict[Rank, int]:
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
            Rank.JACK: 7,
        }


class Suit(Enum):
    CLUBS = 1
    HEARTS = 2
    DIAMONDS = 3
    SPADES = 4

    @staticmethod
    def suits() -> Dict[str, Suit]:
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

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Player):
            return False

        return self.name == other.name and self.hand == other.hand

    @staticmethod
    def generate_name() -> str:
        """Generates a random, pronouncable name for a player.

        :return: A random name.
        """

        vowels = ["a", "e", "o"] * 2 + ["i", "u"]
        consonants = ["b", "d", "f", "g", "h", "k", "l", "m", "n", "p", "qu", "r", "s", "t", "v", "y"]

        suffices = ["d", "h", "l", "n", "s"]

        # The core of the name is a random amount of consonant+vowel combinations.
        syllables = random.randint(2, 3)
        name = "".join([random.choice(consonants) + random.choice(vowels) for _ in range(syllables)])

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
    seed: Optional[int] = None

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

    def __repr__(self) -> str:
        return repr(self.cards)

    def __eq__(self, other: object) -> bool:
        # In case different seeds result in the same card order,
        # we should of course consider the decks equal anyway.
        return self.cards == other.cards if isinstance(other, type(self)) else False


class RuleSet(Enum):
    AMSTERDAM = "Amsterdam"
    ROTTERDAM = "Rotterdam"


class Deal(object):
    players: List[Player]
    bidder_index: int
    trump_suit: Optional[Suit]
    rules: RuleSet
    tricks: List[Trick]

    def __init__(
            self, players: List[Player], bidder_index: int, trump_suit: Suit = None, rules: RuleSet = RuleSet.ROTTERDAM
    ):
        """
        Initializes a Deal (i.e. a sequence of 8 tricks).
        :param players: The players present in this deal. The order of the players is the order in which
            cards must be played in the 8 tricks that compose this Deal. Note that the first trick need
            not be played by the player at index 0; the bidder_index parameter controls this.
        :param bidder_index: The index of the bidding player, i.e. the player that decides the trump suit
            and leads the first trick.
        :param trump_suit: Set the trump suit for this deal. Typically, we do not know the trump suit yet
            on initialization, since the bidding player has yet to pick a suit. Hence, it is an optional argument.
        """

        assert len(players) == 4, f"Invalid amount of players: {len(players)}"
        assert 0 <= bidder_index < 4, f"Invalid bidder index: {bidder_index}"
        assert trump_suit is None or isinstance(trump_suit, Suit), f"Invalid trump suit: {trump_suit}"
        self.players = players
        self.bidder_index = bidder_index
        self.trump_suit = trump_suit
        self.rules = rules
        self.tricks = []

        if self.trump_suit is None:
            user_input = input("Select trump suit (H, D, C, S): ")
            self.trump_suit = Suit.suits()[user_input]

        # The first trick is always started by the bidder.
        trick = Trick(deal=self, leading_player_index=self.bidder_index)
        self.tricks.append(trick)

    def get_teammate_index(self, player: Player) -> int:
        for index, value in enumerate(self.players):
            if value == player:
                return (index + 2) % 4

        raise ValueError("Given player is not in the player list for this deal")

    @property
    def current_trick(self) -> Trick:
        """
        Get the current trick. Returns None if no Trick has started yet or the final Trick has already ended.
        :return: The Trick.
        """

        return None if not self.tricks else self.tricks[-1]

    def new_trick(self) -> None:
        """Start a new trick in this Deal."""
        if self.current_trick:
            assert self.current_trick.has_ended, "Cannot start a new trick if the previous has not ended"

        if not self.players[self.current_trick.winning_card_index].hand:
            # All cards have been played. This will end the Deal.
            # TODO: Implement the point system, automatically start a new Deal if needed, and so on.
            return

        new_trick = Trick(self, leading_player_index=self.current_trick.winning_card_index)
        self.tricks.append(new_trick)


class Trick(object):
    """
    A Trick object represents the state of a single trick within a Deal.
    A Deal essentially contains 8 tricks in total.
    """

    leading_player_index: int
    deal: Deal
    played_cards: List[Optional[Card]]
    has_ended: bool = False

    def __init__(self, deal: Deal, leading_player_index: int):
        assert 0 <= leading_player_index < 4

        self.deal = deal
        self.leading_player_index = leading_player_index

        """
        We initialize the played cards to None so that we can avoid KeyErrors,
        as well as assign played cards according to the same indices as the player list.
        This way we can be sure that even if the trick starts with the third player, we
        do not need a dictionary (or similar construct) to map the played cards to the players.
        """
        self.played_cards = [None, None, None, None]

    @property
    def led_suit(self) -> Optional[Suit]:
        """
        Get the suit with which this trick was led. Equal to the first card played in this trick.
        Returns None if no card has been played yet in this trick.

        :return: Suit
        """
        led_card: Optional[Card] = self.played_cards[self.leading_player_index]

        return None if led_card is None else led_card.suit

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

        :return: The set of legal cards that can be played.
        """
        hand = self.deal.players[self.player_index_to_play].hand

        # When leading, any card in hand is legal.
        if self.led_suit is None:
            return hand

        # Determine the cards that follow the led suit or are higher trump cards than those
        # that are already played (if any; otherwise, all trump cards are logically higher).
        follow_suit_cards = {card for card in hand if card.suit == self.led_suit}
        higher_trump_cards = {
            card
            for card in hand
            if card.suit == self.deal.trump_suit
               and (self.winning_card is None or self.compare_cards(card, self.winning_card) == -1)
        }
        non_trump_cards = {card for card in hand if card.suit != self.deal.trump_suit}

        # If the led suit is the trump suit, only higher trumps are allowed (if available).
        if self.deal.trump_suit == self.led_suit and higher_trump_cards:
            return higher_trump_cards

        # If the player can follow suit, those cards are the only legal ones.
        if follow_suit_cards:
            return follow_suit_cards

        # Suit cannot be followed. We have to determine whether we need to play a higher trump,
        # or whether the rest of our hand is legal.

        if self.deal.rules == RuleSet.ROTTERDAM and higher_trump_cards:
            return higher_trump_cards

        if self.deal.rules == RuleSet.AMSTERDAM and (non_trump_cards or higher_trump_cards):
            # There are either non-trump cards or higher trump cards that we can legally play.
            # We must decide whether we are forced to play a higher trump (if available).
            if self.winning_card_index == self.deal.get_teammate_index(self.deal.players[self.player_index_to_play]):
                # The teammate is currently leading this trick. In Amsterdam games, this means
                # we do not need to play a higher trump, but non-trump cards are also legel.
                return higher_trump_cards.union(non_trump_cards)
            elif higher_trump_cards:
                return higher_trump_cards
            else:
                return non_trump_cards

        # If the player has no higher trump cards, but does have non-trump cards
        # left in his hand, then those cards are legal to play. If the player, however,
        # has no such non-trump cards, then the player has only lower trump cards left.
        # In that scenario all those non-trump cards (i.e. the full hand) is available.
        return non_trump_cards if non_trump_cards else hand

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
            winning_card: Optional[Card] = None if winning_index is None else self.played_cards[winning_index]
            if card is not None and (winning_card is None or self.compare_cards(winning_card, card) == 1):
                winning_index = index

        return winning_index

    @property
    def winning_card(self) -> Optional[Card]:
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

            if card_1.suit == self.deal.trump_suit:
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
        if card_1.suit == self.deal.trump_suit:
            return -1
        if card_2.suit == self.deal.trump_suit:
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
        assert (
                self.played_cards[self.player_index_to_play] is None
        ), f"Player index {self.player_index_to_play} already played a card this trick"

        # The card must be legal to play
        assert card in self.legal_cards, f"Card {card} is not legal to play"

        # Remove the card from the player's hand.
        self.deal.players[self.player_index_to_play].hand.remove(card)

        # Add the card to the trick.
        self.played_cards[self.player_index_to_play] = card

        # If everyone has played a card, the trick is finished.
        if None not in self.played_cards:
            self.end()

    def end(self):
        """
        This function is called when all cards have been played in this Trick.
        We can count points here, detect which player was the winner of the Trick,
        and tell the Deal to start a new Trick (if necessary).
        """
        self.has_ended = True
        self.deal.new_trick()
