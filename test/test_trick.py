import unittest

from models import Player, Trick, Card, Rank, Suit


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

    def test_a_card_can_be_played_in_a_trick(self):
        players = [Player(), Player(), Player(), Player()]
        trick = Trick(players=players, leading_player_index=0)

        players[0].hand = {Card(suit=Suit.SPADES, rank=Rank.ACE)}
        trick.play(Card(suit=Suit.SPADES, rank=Rank.ACE))

        # The turn must shift to the next player
        self.assertEqual(1, trick.player_index_to_play)
        # The card must be removed from the player's hand
        self.assertEqual(0, len(players[0].hand))
        # The card resides within the played cards of the trick
        self.assertEqual(True, Card(suit=Suit.SPADES, rank=Rank.ACE) in trick.played_cards)


if __name__ == "__main__":
    unittest.main()
