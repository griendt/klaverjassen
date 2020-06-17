import unittest
import random

from structs.card import Deck


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

if __name__ == '__main__':
    unittest.main()
