import unittest
import random

from models.card import Card
from models.cardCollection import CardCollection
from models.deck import Deck
from models.player import Player
from models.rank import Rank
from models.suit import Suit


class DeckTestCase(unittest.TestCase):
    def test_deck_initialisation(self):
        deck = Deck()

        # We assume a Piquet deck which has 32 cards.
        self.assertEqual(len(deck.cards), 32)

        # The collection of cards must be unique.
        self.assertEqual(len(set(deck.cards)), 32)

    def test_deck_random_shuffle(self):
        deck_1, deck_2 = Deck(), Deck()

        deck_1.shuffle()
        deck_2.shuffle()

        # This is technically a flaky test since both decks
        # could be identical, but the odds of this are 1 in 52!.
        self.assertNotEqual(deck_1.cards, deck_2.cards)

    def test_deck_shuffle_with_seed(self):
        deck_1, deck_2, deck_3 = Deck(), Deck(), Deck()
        seed_1, seed_2 = random.randint(0, 100000), random.randint(0, 100000)
        deck_1.shuffle(seed_1)
        deck_2.shuffle(seed_1)
        deck_3.shuffle(seed_2)

        # Identical seeds must lead to identical shuffles.
        self.assertEqual(deck_1.cards, deck_2.cards)

        # Different seeds should lead to different shuffles.
        # This is technically a flaky test but the odds of this test
        # failing despite functioning as intended is 1 in 52!.
        self.assertNotEqual(deck_1.cards, deck_3.cards)

    def test_deck_reshuffle_is_possible(self):
        deck_1, deck_2 = Deck(), Deck()
        seed = random.randint(0, 100000)

        deck_1.shuffle(seed)
        deck_2.shuffle(seed)

        # Shuffling twice should yield a different deck.
        # This is technically a flaky test but the odds of this test
        # failing despite functioning as intended is 1 in 52!.
        deck_2.shuffle(seed)
        self.assertNotEqual(deck_1.cards, deck_2.cards)

    def test_card_collections_can_be_equal(self):
        hand_1 = CardCollection([Card(suit=Suit.HEARTS, rank=Rank.ACE), Card(suit=Suit.CLUBS, rank=Rank.JACK),])

        hand_2 = CardCollection([Card(suit=Suit.HEARTS, rank=Rank.ACE), Card(suit=Suit.CLUBS, rank=Rank.JACK),])

        self.assertEqual(hand_1, hand_2)

    def test_equal_card_collections_can_have_different_order(self):
        hand_1 = CardCollection([Card(suit=Suit.HEARTS, rank=Rank.ACE), Card(suit=Suit.CLUBS, rank=Rank.JACK),])

        hand_2 = CardCollection([Card(suit=Suit.CLUBS, rank=Rank.JACK), Card(suit=Suit.HEARTS, rank=Rank.ACE),])

        self.assertEqual(hand_1, hand_2)

    def test_decks_are_equal_only_if_their_cards_are_equally_ordered(self):
        deck_1 = Deck(
            cards=CardCollection([Card(suit=Suit.HEARTS, rank=Rank.ACE), Card(suit=Suit.CLUBS, rank=Rank.JACK),])
        )

        deck_2 = Deck(
            cards=CardCollection([Card(suit=Suit.HEARTS, rank=Rank.ACE), Card(suit=Suit.CLUBS, rank=Rank.JACK),])
        )

        self.assertEqual(deck_1, deck_2)

    def test_a_deck_cannot_be_dealt_if_not_evenly(self):
        deck = Deck()
        players = [Player(), Player(), Player()]

        # What we are testing is the scenario where the deck's cards cannot
        # be dealt evenly among the players, so we must assert it.
        self.assertNotEqual(len(deck.cards) % len(players), 0)

        # In this scenario, the method should throw a ValueError.
        self.assertRaises(ValueError, deck.deal, players)

    def test_a_deck_can_be_dealt(self):
        deck = Deck()
        players = [Player(), Player(), Player(), Player()]
        deck.deal(players)

        # The deck is fully depleted
        self.assertEqual(0, len(deck.cards))
        for player in players:
            # Each player has the required amount of cards
            self.assertEqual(8, len(player.hand))


if __name__ == "__main__":
    unittest.main()
