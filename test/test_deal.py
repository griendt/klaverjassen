import unittest
from unittest.mock import patch

from models import Player, Deal, Suit


class RoundTestCase(unittest.TestCase):
    def test_a_round_can_be_initialized(self) -> None:
        players = [Player(), Player(), Player(), Player()]
        for bidder_index in range(4):
            deal = Deal(players=players, bidder_index=bidder_index)
            self.assertEqual(True, isinstance(deal, Deal))

    def test_a_round_throws_an_error_when_initialized_with_bad_info(self) -> None:
        players = [Player(), Player(), Player()]

        for bidder_index in range(4):
            # No matter who is supposed to start, a round with not exactly 4 players cannot be instantiated.
            self.assertRaises(AssertionError, lambda: Deal(players=players, bidder_index=bidder_index))

        players = [Player(), Player(), Player(), Player()]

        # Bad bidder indices are not allowed.
        self.assertRaises(AssertionError, lambda: Deal(players=players, bidder_index=-1))
        self.assertRaises(AssertionError, lambda: Deal(players=players, bidder_index=4))

        # Invalid suits are not allowed.
        self.assertRaises(AssertionError, lambda: Deal(players=players, bidder_index=0, trump_suit=-1))  # type: ignore

    def test_a_round_can_be_initialized_with_preset_trump_suit(self) -> None:
        players = [Player(), Player(), Player(), Player()]

        for suit in Suit:
            deal = Deal(players=players, bidder_index=0, trump_suit=suit)
            self.assertEqual(True, isinstance(deal, Deal))

    def test_a_round_asks_for_trump_suit_when_started(self) -> None:
        players = [Player(), Player(), Player(), Player()]

        suit_identifier: str
        suit: Suit
        for (suit_identifier, suit) in Suit.suits().items():
            with patch("builtins.input", return_value=suit_identifier):
                deal = Deal(players=players, bidder_index=0)
                deal.initialize()

                self.assertEqual(deal.trump_suit, suit)

    def test_a_round_fails_to_start_if_invalid_trump_suit_is_given(self) -> None:
        def bad_initialization() -> None:
            players = [Player(), Player(), Player(), Player()]
            with patch("builtins.input", return_value="bad_suit"):
                deal = Deal(players=players, bidder_index=0)
                deal.initialize()

        self.assertRaises(KeyError, bad_initialization)

    def test_a_deal_can_return_the_teammate_of_a_player(self) -> None:
        players = [Player(name="1"), Player(name="2"), Player(name="3"), Player(name="4")]
        deal = Deal(players=players, bidder_index=0)

        self.assertEqual(2, deal.get_teammate_index(Player(name="1")))
        self.assertEqual(3, deal.get_teammate_index(Player(name="2")))
        self.assertEqual(0, deal.get_teammate_index(Player(name="3")))
        self.assertEqual(1, deal.get_teammate_index(Player(name="4")))

    def test_a_deal_throws_an_error_if_an_invalid_player_requests_his_teammate(self) -> None:
        players = [Player(name="1"), Player(name="2"), Player(name="3"), Player(name="4")]
        deal = Deal(players=players, bidder_index=0)
        unknown_player = Player(name="5")
        self.assertRaises(ValueError, deal.get_teammate_index, [unknown_player])


if __name__ == "__main__":
    unittest.main()
