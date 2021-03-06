import unittest

from models import Player


class PlayerTestCase(unittest.TestCase):
    def test_player_creation_with_name(self) -> None:
        player = Player(hand=set(), name="Foo")
        self.assertEqual(player.name, "Foo")

    def test_player_creation_with_random_name(self) -> None:
        for x in range(100):
            player = Player(hand=set())

            # The name is set despite it not being specified in initialisation
            self.assertIsNotNone(player.name)

            # Randomly generated names are between 4-11 characters
            self.assertGreater(len(player.name), 3)
            self.assertLess(len(player.name), 12)

    def test_player_creation_without_hand_specified(self) -> None:
        player = Player(name="Foo")
        self.assertEqual(player.hand, set())


if __name__ == "__main__":
    unittest.main()
