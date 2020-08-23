import unittest
from unittest.mock import patch

from models import Player, Deal, Suit, Card, Rank


class DealTestCase(unittest.TestCase):
    def test_a_deal_can_be_initialized(self) -> None:
        players = [Player(), Player(), Player(), Player()]
        for bidder_index in range(4):
            deal = Deal(players=players, bidder_index=bidder_index, trump_suit=Suit.SPADES)
            self.assertEqual(True, isinstance(deal, Deal))

    def test_a_deal_throws_an_error_when_initialized_with_bad_info(self) -> None:
        players = [Player(), Player(), Player()]

        for bidder_index in range(4):
            # No matter who is supposed to start, a deal with not exactly 4 players cannot be instantiated.
            self.assertRaises(AssertionError, lambda: Deal(players=players, bidder_index=bidder_index))

        players = [Player(), Player(), Player(), Player()]

        # Bad bidder indices are not allowed.
        self.assertRaises(AssertionError, lambda: Deal(players=players, bidder_index=-1))
        self.assertRaises(AssertionError, lambda: Deal(players=players, bidder_index=4))

        # Invalid suits are not allowed.
        # noinspection PyTypeChecker
        self.assertRaises(AssertionError, lambda: Deal(players=players, bidder_index=0, trump_suit=-1))  # type: ignore

    def test_a_deal_can_be_initialized_with_preset_trump_suit(self) -> None:
        players = [Player(), Player(), Player(), Player()]

        for suit in Suit:
            deal = Deal(players=players, bidder_index=0, trump_suit=suit)
            self.assertEqual(True, isinstance(deal, Deal))

    def test_a_deal_asks_for_trump_suit_when_started(self) -> None:
        players = [Player(), Player(), Player(), Player()]

        suit_identifier: str
        suit: Suit
        for (suit_identifier, suit) in Suit.suits().items():
            with patch("builtins.input", return_value=suit_identifier):
                deal = Deal(players=players, bidder_index=0)

                self.assertEqual(deal.trump_suit, suit)

    def test_a_deal_fails_to_start_if_invalid_trump_suit_is_given(self) -> None:
        def bad_initialization() -> None:
            players = [Player(), Player(), Player(), Player()]
            with patch("builtins.input", return_value="bad_suit"):
                _ = Deal(players=players, bidder_index=0)

        self.assertRaises(KeyError, bad_initialization)

    def test_a_deal_can_return_the_teammate_of_a_player(self) -> None:
        players = [Player(name="1"), Player(name="2"), Player(name="3"), Player(name="4")]
        deal = Deal(players=players, bidder_index=0, trump_suit=Suit.SPADES)

        self.assertEqual(2, deal.get_teammate_index(Player(name="1")))
        self.assertEqual(3, deal.get_teammate_index(Player(name="2")))
        self.assertEqual(0, deal.get_teammate_index(Player(name="3")))
        self.assertEqual(1, deal.get_teammate_index(Player(name="4")))

    def test_a_deal_throws_an_error_if_an_invalid_player_requests_his_teammate(self) -> None:
        players = [Player(name="1"), Player(name="2"), Player(name="3"), Player(name="4")]
        deal = Deal(players=players, bidder_index=0, trump_suit=Suit.SPADES)
        unknown_player = Player(name="5")
        self.assertRaises(ValueError, deal.get_teammate_index, [unknown_player])

    def test_no_new_trick_is_started_when_all_cards_are_played(self) -> None:
        players = [Player(name="1"), Player(name="2"), Player(name="3"), Player(name="4")]
        deal = Deal(players=players, bidder_index=0, trump_suit=Suit.HEARTS)
        trick = deal.current_trick

        players[0].hand = {Card(suit=Suit.SPADES, rank=Rank.JACK)}
        players[1].hand = {Card(suit=Suit.SPADES, rank=Rank.TEN)}
        players[2].hand = {Card(suit=Suit.SPADES, rank=Rank.KING)}
        players[3].hand = {Card(suit=Suit.DIAMONDS, rank=Rank.SEVEN)}

        trick.play(Card(suit=Suit.SPADES, rank=Rank.JACK))
        trick.play(Card(suit=Suit.SPADES, rank=Rank.TEN))
        trick.play(Card(suit=Suit.SPADES, rank=Rank.KING))
        trick.play(Card(suit=Suit.DIAMONDS, rank=Rank.SEVEN))

        self.assertEqual(1, len(deal.tricks))

    def test_a_new_trick_is_started_when_there_are_cards_left_to_play(self) -> None:
        players = [Player(name="1"), Player(name="2"), Player(name="3"), Player(name="4")]
        deal = Deal(players=players, bidder_index=0, trump_suit=Suit.HEARTS)
        trick = deal.current_trick

        players[0].hand = {Card(suit=Suit.SPADES, rank=Rank.JACK), Card(suit=Suit.SPADES, rank=Rank.QUEEN)}
        players[1].hand = {Card(suit=Suit.SPADES, rank=Rank.TEN), Card(suit=Suit.SPADES, rank=Rank.EIGHT)}
        players[2].hand = {Card(suit=Suit.SPADES, rank=Rank.KING), Card(suit=Suit.SPADES, rank=Rank.SEVEN)}
        players[3].hand = {Card(suit=Suit.DIAMONDS, rank=Rank.SEVEN), Card(suit=Suit.DIAMONDS, rank=Rank.EIGHT)}

        trick.play(Card(suit=Suit.SPADES, rank=Rank.JACK))
        trick.play(Card(suit=Suit.SPADES, rank=Rank.TEN))
        trick.play(Card(suit=Suit.SPADES, rank=Rank.KING))
        trick.play(Card(suit=Suit.DIAMONDS, rank=Rank.SEVEN))

        self.assertEqual(2, len(deal.tricks))
        self.assertEqual(1, deal.current_trick.player_index_to_play)
        self.assertEqual(1, deal.current_trick.leading_player_index)


if __name__ == "__main__":
    unittest.main()
