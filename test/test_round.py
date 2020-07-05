import unittest

from models.player import Player
from models.round import Round

class RoundTestCase(unittest.TestCase):

    def rounds_can_be_initialized(self):
        players = [Player(), Player(), Player(), Player()]
        for bidder_index in range(4):
            round = Round(players=players, bidder_index=bidder_index)
            self.assertEqual(True, isinstance(round, Round))

    def test_a_round_throws_an_error_when_initialized_with_bad_info(self):
        players = [Player(), Player(), Player()]

        for bidder_index in range(4):
            # No matter who is supposed to start, a round with not exactly 4 players cannot be instantiated.
            self.assertRaises(AssertionError, lambda: Round(players=players, bidder_index=bidder_index))

        players = [Player(), Player(), Player(), Player()]

        # Bad bidder indices are not allowed.
        self.assertRaises(AssertionError, lambda: Round(players=players, bidder_index=-1))
        self.assertRaises(AssertionError, lambda: Round(players=players, bidder_index=4))


if __name__ == '__main__':
    unittest.main()
