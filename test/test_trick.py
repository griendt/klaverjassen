import unittest

from models import Player, Trick


class RoundTestCase(unittest.TestCase):

    def test_trick_initialization(self):
        players = [Player(), Player(), Player(), Player()]
        trick = Trick(players=players, leading_player_index=0)

        self.assertEqual(True, isinstance(trick, Trick))

    def test_tricks_initialization_fails_with_bad_parameters(self):
        def init_trick_with_invalid_players():
            players = [Player(), Player(), Player(), Player(), Player()]
            trick = Trick(players=players, leading_player_index=0)

        def init_trick_with_invalid_leading_player_index():
            players = [Player(), Player(), Player(), Player(), ]
            trick = Trick(players=players, leading_player_index=4)

        self.assertRaises(AssertionError, init_trick_with_invalid_players)
        self.assertRaises(AssertionError, init_trick_with_invalid_leading_player_index)

    def test_a_trick_without_played_cards_has_no_leading_suit(self):
        players = [Player(), Player(), Player(), Player()]
        trick = Trick(players=players, leading_player_index=0)

        self.assertEqual(None, trick.led_suit)


if __name__ == "__main__":
    unittest.main()
