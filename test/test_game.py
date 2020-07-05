import unittest

from interaction import mock_input
from models import Player, Game, Suit


class RoundTestCase(unittest.TestCase):
    def test_a_round_can_be_initialized(self):
        players = [Player(), Player(), Player(), Player()]
        for bidder_index in range(4):
            game = Game(players=players, bidder_index=bidder_index)
            self.assertEqual(True, isinstance(game, Game))

    def test_a_round_throws_an_error_when_initialized_with_bad_info(self):
        players = [Player(), Player(), Player()]

        for bidder_index in range(4):
            # No matter who is supposed to start, a round with not exactly 4 players cannot be instantiated.
            self.assertRaises(AssertionError, lambda: Game(players=players, bidder_index=bidder_index))

        players = [Player(), Player(), Player(), Player()]

        # Bad bidder indices are not allowed.
        self.assertRaises(AssertionError, lambda: Game(players=players, bidder_index=-1))
        self.assertRaises(AssertionError, lambda: Game(players=players, bidder_index=4))

        # Invalid suits are not allowed.
        self.assertRaises(AssertionError, lambda: Game(players=players, bidder_index=0, trump_suit=-1))

    def test_a_round_can_be_initialized_with_preset_trump_suit(self):
        players = [Player(), Player(), Player(), Player()]

        for suit in Suit:
            game = Game(players=players, bidder_index=0, trump_suit=suit)
            self.assertEqual(True, isinstance(game, Game))

    def test_a_round_asks_for_trump_suit_when_started(self):
        players = [Player(), Player(), Player(), Player()]

        suit_identifier: str
        suit: Suit
        for (suit_identifier, suit) in Suit.suits().items():
            with mock_input(suit_identifier):
                game = Game(players=players, bidder_index=0)
                game.initialize()

                self.assertEqual(game.trump_suit, suit)

    def test_a_round_fails_to_start_if_invalid_trump_suit_is_given(self):
        def bad_initialization():
            players = [Player(), Player(), Player(), Player()]
            with mock_input("bad_suit"):
                game = Game(players=players, bidder_index=0)
                game.initialize()

        self.assertRaises(KeyError, bad_initialization)


if __name__ == "__main__":
    unittest.main()
