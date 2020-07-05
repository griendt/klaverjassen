import unittest

from models.player import Player


class PlayerTestCase(unittest.TestCase):
    def test_player_creation_with_name(self):
        player = Player(hand=[], name="Foo")
        self.assertEqual(player.name, "Foo")

    def test_player_creation_with_random_name(self):
        for x in range(100):
            player = Player(hand=[])

            # The name is set despite it not being specified in initialisation
            self.assertIsNotNone(player.name)

            # Randomly generated names are between 4-11 characters
            self.assertGreater(len(player.name), 3)
            self.assertLess(len(player.name), 12)

    def test_player_creation_without_hand_specified(self):
        player = Player(name="Foo")
        self.assertEqual(player.hand, [])


if __name__ == "__main__":
    unittest.main()
