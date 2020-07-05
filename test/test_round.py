import unittest

from models.player import Player
from models.round import Round
from models.suit import Suit


class RoundTestCase(unittest.TestCase):
    def test_a_round_can_be_initialized(self):
        players = [Player(), Player(), Player(), Player()]
        for bidder_index in range(4):
            Round(players=players, bidder_index=bidder_index)

    def test_a_round_throws_an_error_when_initialized_with_bad_info(self):
        players = [Player(), Player(), Player()]

        for bidder_index in range(4):
            # No matter who is supposed to start, a round with not exactly 4 players cannot be instantiated.
            self.assertRaises(AssertionError, lambda: Round(players=players, bidder_index=bidder_index))

        players = [Player(), Player(), Player(), Player()]

        # Bad bidder indices are not allowed.
        self.assertRaises(AssertionError, lambda: Round(players=players, bidder_index=-1))
        self.assertRaises(AssertionError, lambda: Round(players=players, bidder_index=4))

        # Invalid suits are not allowed.
        self.assertRaises(AssertionError, lambda: Round(players=players, bidder_index=0, trump_suit=-1))

    def test_a_round_can_be_initialized_with_preset_trump_suit(self):
        players = [Player(), Player(), Player(), Player()]

        for suit in Suit:
            Round(players=players, bidder_index=0, trump_suit=suit)


if __name__ == "__main__":
    unittest.main()
