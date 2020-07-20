import unittest
from itertools import product

from models import Player, Trick, Card, Rank, Suit, Game


class RoundTestCase(unittest.TestCase):
    def test_trick_initialization(self) -> None:
        players = [Player(), Player(), Player(), Player()]
        game = Game(players=players, bidder_index=0)
        trick = Trick(game=game, leading_player_index=0)

        self.assertEqual(True, isinstance(trick, Trick))

    def test_tricks_initialization_fails_with_bad_parameters(self) -> None:
        def init_trick_with_invalid_players() -> None:
            players = [Player(), Player(), Player(), Player(), Player()]
            game = Game(players=players, bidder_index=0)
            Trick(game=game, leading_player_index=0)

        def init_trick_with_invalid_leading_player_index() -> None:
            players = [Player(), Player(), Player(), Player()]
            game = Game(players=players, bidder_index=0)
            Trick(game=game, leading_player_index=4)

        self.assertRaises(AssertionError, init_trick_with_invalid_players)
        self.assertRaises(AssertionError, init_trick_with_invalid_leading_player_index)

    def test_a_trick_without_played_cards_has_no_leading_suit(self) -> None:
        players = [Player(), Player(), Player(), Player()]
        game = Game(players=players, bidder_index=0)
        trick = Trick(game=game, leading_player_index=0)

        self.assertEqual(None, trick.led_suit)

    def test_the_highest_card_in_a_trick_without_trumps(self) -> None:
        players = [Player(), Player(), Player(), Player()]
        game = Game(players=players, bidder_index=0, trump_suit=Suit.HEARTS)
        trick = Trick(game=game, leading_player_index=0)

        players[0].hand = {Card(suit=Suit.SPADES, rank=Rank.JACK)}
        players[1].hand = {Card(suit=Suit.SPADES, rank=Rank.TEN)}
        players[2].hand = {Card(suit=Suit.SPADES, rank=Rank.KING)}
        players[3].hand = {Card(suit=Suit.DIAMONDS, rank=Rank.ACE)}
        trick.play(Card(suit=Suit.SPADES, rank=Rank.JACK))
        trick.play(Card(suit=Suit.SPADES, rank=Rank.TEN))
        trick.play(Card(suit=Suit.SPADES, rank=Rank.KING))
        trick.play(Card(suit=Suit.DIAMONDS, rank=Rank.ACE))

        # Player 4 played an ace, but it is in the wrong suit.
        # Player 1 played a jack, but it is not the trump suit, so the 10 wins.
        self.assertEqual(1, trick.winning_card_index)
        self.assertEqual(Card(suit=Suit.SPADES, rank=Rank.TEN), trick.winning_card)

    def test_the_highest_card_in_a_trick_with_trumps(self) -> None:
        players = [Player(), Player(), Player(), Player()]
        game = Game(players=players, bidder_index=0, trump_suit=Suit.DIAMONDS)
        trick = Trick(game=game, leading_player_index=0)

        players[0].hand = {Card(suit=Suit.SPADES, rank=Rank.JACK)}
        players[1].hand = {Card(suit=Suit.SPADES, rank=Rank.TEN)}
        players[2].hand = {Card(suit=Suit.SPADES, rank=Rank.KING)}
        players[3].hand = {Card(suit=Suit.DIAMONDS, rank=Rank.SEVEN)}
        trick.play(Card(suit=Suit.SPADES, rank=Rank.JACK))
        trick.play(Card(suit=Suit.SPADES, rank=Rank.TEN))
        trick.play(Card(suit=Suit.SPADES, rank=Rank.KING))
        trick.play(Card(suit=Suit.DIAMONDS, rank=Rank.SEVEN))

        # Player 4 played a seven, but because it is a trump card, he will win.
        self.assertEqual(3, trick.winning_card_index)
        self.assertEqual(Card(suit=Suit.DIAMONDS, rank=Rank.SEVEN), trick.winning_card)

    def test_a_card_can_be_played_in_a_trick(self) -> None:
        players = [Player(), Player(), Player(), Player()]
        game = Game(players=players, bidder_index=0)
        trick = Trick(game=game, leading_player_index=0)

        players[0].hand = {Card(suit=Suit.SPADES, rank=Rank.ACE)}
        trick.play(Card(suit=Suit.SPADES, rank=Rank.ACE))

        # The turn must shift to the next player
        self.assertEqual(1, trick.player_index_to_play)
        # The card must be removed from the player's hand
        self.assertEqual(0, len(players[0].hand))
        # The card resides within the played cards of the trick
        self.assertEqual(True, Card(suit=Suit.SPADES, rank=Rank.ACE) in trick.played_cards)

    def test_a_player_cannot_play_a_card_it_does_not_have(self) -> None:
        def play_bad_card() -> None:
            players = [Player(), Player(), Player(), Player()]
            game = Game(players=players, bidder_index=0)
            trick = Trick(game=game, leading_player_index=0)
            players[0].hand = {Card(suit=Suit.SPADES, rank=Rank.ACE)}

            # The player does not actually have this card; it should throw AssertionError
            trick.play(Card(suit=Suit.HEARTS, rank=Rank.ACE))

        self.assertRaises(AssertionError, play_bad_card)

    def test_a_player_must_follow_suit_if_possible(self) -> None:
        players = [Player(), Player(), Player(), Player()]
        game = Game(players=players, bidder_index=0)
        trick = Trick(game=game, leading_player_index=0)

        players[0].hand = {Card(suit=Suit.SPADES, rank=Rank.ACE)}
        players[1].hand = {
            Card(suit=Suit.SPADES, rank=Rank.KING),
            Card(suit=Suit.SPADES, rank=Rank.QUEEN),
            Card(suit=Suit.HEARTS, rank=Rank.KING),
        }

        trick.play(Card(suit=Suit.SPADES, rank=Rank.ACE))

        # The first player has led spades; the next player should have two legal choices.
        self.assertEqual(
            {Card(suit=Suit.SPADES, rank=Rank.KING), Card(suit=Suit.SPADES, rank=Rank.QUEEN), }, trick.legal_cards
        )

        self.assertEqual(True, Card(suit=Suit.HEARTS, rank=Rank.KING) in game.players[trick.player_index_to_play].hand)
        # If the player attempts to play a different card anyway, then despite holding the card
        # in their hand, it should raise an exception.
        self.assertRaises(AssertionError, trick.play, Card(suit=Suit.HEARTS, rank=Rank.KING))

    def test_a_player_must_not_follow_suit_if_not_possible(self) -> None:
        players = [Player(), Player(), Player(), Player()]
        game = Game(players=players, bidder_index=0)
        trick = Trick(game=game, leading_player_index=0)

        players[0].hand = {Card(suit=Suit.SPADES, rank=Rank.ACE)}
        players[1].hand = {
            Card(suit=Suit.HEARTS, rank=Rank.KING),
            Card(suit=Suit.HEARTS, rank=Rank.QUEEN),
            Card(suit=Suit.DIAMONDS, rank=Rank.KING),
        }

        trick.play(Card(suit=Suit.SPADES, rank=Rank.ACE))

        # The next player may play any of these cards despite them not following suit.
        self.assertEqual(
            {
                Card(suit=Suit.HEARTS, rank=Rank.KING),
                Card(suit=Suit.HEARTS, rank=Rank.QUEEN),
                Card(suit=Suit.DIAMONDS, rank=Rank.KING),
            },
            trick.legal_cards,
        )

        # Playing this card should be acceptable despite it not following suit.
        trick.play(Card(suit=Suit.HEARTS, rank=Rank.KING))

    def test_cards_can_be_compared_before_a_suit_is_led(self) -> None:
        players = [Player(), Player(), Player(), Player()]
        game = Game(players=players, bidder_index=0)
        trick = Trick(game=game, leading_player_index=0)

        # The queen should be consider higher, as we are assuming we are not
        # dealing with a trump suit, given that no trump suit was even specified yet.
        self.assertEqual(
            1, trick.compare_cards(Card(suit=Suit.HEARTS, rank=Rank.JACK), Card(suit=Suit.HEARTS, rank=Rank.QUEEN))
        )

        # Unrelated cards cannot be compared properly without a trump suit or a led suit.
        self.assertEqual(
            0, trick.compare_cards(Card(suit=Suit.HEARTS, rank=Rank.JACK), Card(suit=Suit.SPADES, rank=Rank.ACE), )
        )

        game.trump_suit = Suit.HEARTS

        # Now that we have a trump suit defined, the higher trump should rank higher.
        self.assertEqual(
            -1, trick.compare_cards(Card(suit=Suit.HEARTS, rank=Rank.JACK), Card(suit=Suit.HEARTS, rank=Rank.QUEEN))
        )

    def test_cards_can_be_compared_after_trump_suit_is_led(self) -> None:
        players = [Player(), Player(), Player(), Player()]
        players[0].hand = {Card(suit=Suit.SPADES, rank=Rank.QUEEN)}
        game = Game(players=players, bidder_index=0, trump_suit=Suit.SPADES)
        trick = Trick(game=game, leading_player_index=0)

        # The trick starts with the trump suit.
        trick.play(Card(suit=Suit.SPADES, rank=Rank.QUEEN))

        # The Johnny scores higher than the ten, in contrast to the normal order.
        # Same thing for the Nerf (9).
        self.assertEqual(
            -1, trick.compare_cards(Card(suit=Suit.SPADES, rank=Rank.JACK), Card(suit=Suit.SPADES, rank=Rank.TEN), )
        )
        self.assertEqual(
            -1, trick.compare_cards(Card(suit=Suit.SPADES, rank=Rank.NINE), Card(suit=Suit.SPADES, rank=Rank.TEN), )
        )

        # Any trump card will rank higher than any non-trump card.
        for first_rank, second_rank, second_suit in product(Rank, Rank, Suit):
            # We are testing non-trump cards for the second card, so skip the trump cards.
            if second_suit == game.trump_suit:
                continue

            self.assertEqual(
                -1,
                trick.compare_cards(Card(suit=Suit.SPADES, rank=first_rank),
                                    Card(suit=second_suit, rank=second_rank), ),
            )

        # Any two cards that both aren't trump will be incomparable.
        for first_rank, first_suit, second_rank, second_suit in product(Rank, Suit, Rank, Suit):
            # If the suits match or any equals trump, skip.
            if first_suit == game.trump_suit or second_suit == game.trump_suit or first_suit == second_suit:
                continue

            self.assertEqual(
                0, trick.compare_cards(Card(suit=first_suit, rank=first_rank), Card(suit=second_suit, rank=second_rank))
            )

    def test_cards_can_be_compared_if_non_trump_suit_is_led(self) -> None:
        players = [Player(), Player(), Player(), Player()]
        players[0].hand = {Card(suit=Suit.SPADES, rank=Rank.QUEEN)}
        game = Game(players=players, bidder_index=0, trump_suit=Suit.CLUBS)
        trick = Trick(game=game, leading_player_index=0)

        # The led suit will be Spades, but the trump suit is Clubs.
        trick.play(Card(suit=Suit.SPADES, rank=Rank.QUEEN))

        # Any trump card will rank higher than any non-trump card, regardless whether
        # that other card was in the led suit or not.
        for first_rank, second_rank, second_suit in product(Rank, Rank, Suit):
            # We are testing non-trump cards for the second card, so skip the trump cards.
            if second_suit == game.trump_suit:
                continue

            assert game.trump_suit is not None
            self.assertEqual(
                -1,
                trick.compare_cards(
                    Card(suit=game.trump_suit, rank=first_rank), Card(suit=second_suit, rank=second_rank),
                ),
            )

        # Any card in the led suit beats any other card that is not trump or in the led suit.
        for first_rank, second_rank, second_suit in product(Rank, Rank, Suit):
            # We are testing second cards that are non-trump and not the led suit, so skip those.
            if second_suit == game.trump_suit or second_suit == trick.led_suit:
                continue

            assert trick.led_suit is not None
            self.assertEqual(
                -1,
                trick.compare_cards(
                    Card(suit=trick.led_suit, rank=first_rank), Card(suit=second_suit, rank=second_rank),
                ),
            )

        # Two cards both in the led suit will obey the regular order.
        self.assertEqual(
            -1, trick.compare_cards(Card(suit=Suit.SPADES, rank=Rank.QUEEN), Card(suit=Suit.SPADES, rank=Rank.JACK), )
        )
        self.assertEqual(
            -1, trick.compare_cards(Card(suit=Suit.SPADES, rank=Rank.TEN), Card(suit=Suit.SPADES, rank=Rank.NINE), )
        )

        # Two cards that both are neither trump nor the led suit will be incomparable.
        for first_rank, first_suit, second_rank, second_suit in product(Rank, Suit, Rank, Suit):
            if first_suit in [game.trump_suit, trick.led_suit] or second_suit in [game.trump_suit, trick.led_suit]:
                continue

            self.assertEqual(
                0,
                trick.compare_cards(Card(suit=first_suit, rank=first_rank), Card(suit=second_suit, rank=second_rank), ),
            )

    def test_all_cards_are_legal_if_suit_cannot_be_followed_and_no_trump_is_available(self) -> None:
        players = [Player(), Player(), Player(), Player()]
        players[0].hand = {Card(suit=Suit.SPADES, rank=Rank.QUEEN)}
        players[1].hand = {
            Card(suit=Suit.HEARTS, rank=Rank.QUEEN),
            Card(suit=Suit.HEARTS, rank=Rank.ACE),
            Card(suit=Suit.DIAMONDS, rank=Rank.ACE),
        }
        game = Game(players=players, bidder_index=0, trump_suit=Suit.CLUBS)
        trick = Trick(game=game, leading_player_index=0)

        trick.play(Card(suit=Suit.SPADES, rank=Rank.QUEEN))

        self.assertEqual(
            {
                Card(suit=Suit.HEARTS, rank=Rank.QUEEN),
                Card(suit=Suit.HEARTS, rank=Rank.ACE),
                Card(suit=Suit.DIAMONDS, rank=Rank.ACE),
            },
            trick.legal_cards,
        )

    def test_only_trump_cards_are_legal_if_suit_cannot_be_followed_and_trumps_are_available(self) -> None:
        players = [Player(), Player(), Player(), Player()]
        players[0].hand = {Card(suit=Suit.SPADES, rank=Rank.QUEEN)}
        players[1].hand = {
            Card(suit=Suit.HEARTS, rank=Rank.QUEEN),
            Card(suit=Suit.HEARTS, rank=Rank.ACE),
            Card(suit=Suit.DIAMONDS, rank=Rank.ACE),
        }
        game = Game(players=players, bidder_index=0, trump_suit=Suit.HEARTS)
        trick = Trick(game=game, leading_player_index=0)

        trick.play(Card(suit=Suit.SPADES, rank=Rank.QUEEN))

        self.assertEqual(
            {Card(suit=Suit.HEARTS, rank=Rank.QUEEN), Card(suit=Suit.HEARTS, rank=Rank.ACE), }, trick.legal_cards
        )

    def test_only_cards_of_the_same_suit_are_legal_if_available(self) -> None:
        players = [Player(), Player(), Player(), Player()]
        players[0].hand = {Card(suit=Suit.HEARTS, rank=Rank.NINE)}
        players[1].hand = {
            Card(suit=Suit.HEARTS, rank=Rank.QUEEN),
            Card(suit=Suit.HEARTS, rank=Rank.ACE),
            Card(suit=Suit.DIAMONDS, rank=Rank.ACE),
        }
        game = Game(players=players, bidder_index=0, trump_suit=Suit.DIAMONDS)
        trick = Trick(game=game, leading_player_index=0)

        trick.play(Card(suit=Suit.HEARTS, rank=Rank.NINE))

        self.assertEqual(
            {Card(suit=Suit.HEARTS, rank=Rank.QUEEN), Card(suit=Suit.HEARTS, rank=Rank.ACE), }, trick.legal_cards
        )

    def test_only_higher_trump_cards_are_legal_if_led_suit_is_trump_and_higher_trumps_are_available(self) -> None:
        players = [Player(), Player(), Player(), Player()]
        players[0].hand = {Card(suit=Suit.HEARTS, rank=Rank.KING)}
        players[1].hand = {
            Card(suit=Suit.HEARTS, rank=Rank.QUEEN),
            Card(suit=Suit.HEARTS, rank=Rank.ACE),
            Card(suit=Suit.DIAMONDS, rank=Rank.ACE),
        }
        game = Game(players=players, bidder_index=0, trump_suit=Suit.HEARTS)
        trick = Trick(game=game, leading_player_index=0)

        trick.play(Card(suit=Suit.HEARTS, rank=Rank.KING))

        self.assertEqual({Card(suit=Suit.HEARTS, rank=Rank.ACE), }, trick.legal_cards)

    def test_only_higher_trump_cards_are_legal_if_led_suit_is_unavailable_and_trumps_were_already_played(self) -> None:
        players = [Player(), Player(), Player(), Player()]
        players[0].hand = {Card(suit=Suit.DIAMONDS, rank=Rank.KING)}
        players[1].hand = {Card(suit=Suit.HEARTS, rank=Rank.KING)}
        players[2].hand = {
            Card(suit=Suit.HEARTS, rank=Rank.QUEEN),
            Card(suit=Suit.HEARTS, rank=Rank.ACE),
            Card(suit=Suit.CLUBS, rank=Rank.ACE),
        }
        game = Game(players=players, bidder_index=0, trump_suit=Suit.HEARTS)
        trick = Trick(game=game, leading_player_index=0)

        trick.play(Card(suit=Suit.DIAMONDS, rank=Rank.KING))
        trick.play(Card(suit=Suit.HEARTS, rank=Rank.KING))

        self.assertEqual({Card(suit=Suit.HEARTS, rank=Rank.ACE), }, trick.legal_cards)

    def test_lower_trump_is_allowed_if_led_suit_is_trump_and_no_higher_trumps_are_available(self) -> None:
        players = [Player(), Player(), Player(), Player()]
        players[0].hand = {Card(suit=Suit.HEARTS, rank=Rank.KING)}
        players[1].hand = {
            Card(suit=Suit.HEARTS, rank=Rank.QUEEN),
            Card(suit=Suit.HEARTS, rank=Rank.SEVEN),
            Card(suit=Suit.HEARTS, rank=Rank.EIGHT),
            Card(suit=Suit.CLUBS, rank=Rank.SEVEN),
        }
        game = Game(players=players, bidder_index=0, trump_suit=Suit.HEARTS)
        trick = Trick(game=game, leading_player_index=0)

        trick.play(Card(suit=Suit.HEARTS, rank=Rank.KING))

        self.assertEqual(
            {
                Card(suit=Suit.HEARTS, rank=Rank.QUEEN),
                Card(suit=Suit.HEARTS, rank=Rank.EIGHT),
                Card(suit=Suit.HEARTS, rank=Rank.SEVEN),
            },
            trick.legal_cards,
        )

    def test_lower_trump_is_allowed_if_no_other_cards_are_in_hand(self) -> None:
        players = [Player(), Player(), Player(), Player()]
        players[0].hand = {Card(suit=Suit.HEARTS, rank=Rank.KING)}
        players[1].hand = {Card(suit=Suit.DIAMONDS, rank=Rank.ACE)}
        players[2].hand = {
            Card(suit=Suit.DIAMONDS, rank=Rank.TEN),
            Card(suit=Suit.DIAMONDS, rank=Rank.KING),
            Card(suit=Suit.DIAMONDS, rank=Rank.QUEEN),
            Card(suit=Suit.DIAMONDS, rank=Rank.EIGHT),
            Card(suit=Suit.DIAMONDS, rank=Rank.SEVEN),
        }
        game = Game(players=players, bidder_index=0, trump_suit=Suit.DIAMONDS)
        trick = Trick(game=game, leading_player_index=0)

        trick.play(Card(suit=Suit.HEARTS, rank=Rank.KING))
        trick.play(Card(suit=Suit.DIAMONDS, rank=Rank.ACE))

        self.assertEqual(
            {
                Card(suit=Suit.DIAMONDS, rank=Rank.TEN),
                Card(suit=Suit.DIAMONDS, rank=Rank.KING),
                Card(suit=Suit.DIAMONDS, rank=Rank.QUEEN),
                Card(suit=Suit.DIAMONDS, rank=Rank.EIGHT),
                Card(suit=Suit.DIAMONDS, rank=Rank.SEVEN),
            },
            trick.legal_cards,
        )

    def test_winning_card_detection_returns_none_if_no_card_was_played(self) -> None:
        players = [Player(), Player(), Player(), Player()]
        game = Game(players=players, bidder_index=0, trump_suit=Suit.DIAMONDS)
        trick = Trick(game=game, leading_player_index=0)

        self.assertEqual(None, trick.winning_card)
        self.assertEqual(None, trick.winning_card_index)

    def test_winning_card_can_be_done_for_incomplete_tricks(self) -> None:
        players = [Player(), Player(), Player(), Player()]
        players[0].hand = {Card(suit=Suit.HEARTS, rank=Rank.KING)}
        players[1].hand = {Card(suit=Suit.HEARTS, rank=Rank.TEN)}
        players[2].hand = {Card(suit=Suit.HEARTS, rank=Rank.NINE)}
        players[3].hand = {Card(suit=Suit.HEARTS, rank=Rank.ACE)}
        game = Game(players=players, bidder_index=0, trump_suit=Suit.DIAMONDS)
        trick = Trick(game=game, leading_player_index=0)

        trick.play(Card(suit=Suit.HEARTS, rank=Rank.KING))
        self.assertEqual(Card(suit=Suit.HEARTS, rank=Rank.KING), trick.winning_card)
        trick.play(Card(suit=Suit.HEARTS, rank=Rank.TEN))
        self.assertEqual(Card(suit=Suit.HEARTS, rank=Rank.TEN), trick.winning_card)
        trick.play(Card(suit=Suit.HEARTS, rank=Rank.NINE))
        self.assertEqual(Card(suit=Suit.HEARTS, rank=Rank.TEN), trick.winning_card)
        trick.play(Card(suit=Suit.HEARTS, rank=Rank.ACE))
        self.assertEqual(Card(suit=Suit.HEARTS, rank=Rank.ACE), trick.winning_card)


if __name__ == "__main__":
    unittest.main()
