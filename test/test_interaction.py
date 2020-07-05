import unittest

from interaction import mock_input


class Interaction(unittest.TestCase):

    def test_input_can_be_mocked(self):
        with mock_input("mocked_value"):
            test_value = input("Insert a value")

        # The mock_input method patches input() to return the specified value automatically.
        self.assertEqual("mocked_value", test_value)


if __name__ == "__main__":
    unittest.main()
