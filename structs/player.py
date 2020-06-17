import random

from structs.card import CardCollection


class Player(object):
    hand: CardCollection
    name: str

    def __init__(self, hand: CardCollection, name: str = None):
        self.hand = hand
        self.name = name if name is not None else self.generate_name()

    @staticmethod
    def generate_name() -> str:
        """Generates a random, pronouncable name for a player."""
        vowels = ["a", "e", "o"] * 2 + ["i", "u"]
        consonants = ["b", "d", "f", "g", "h", "k", "l", "m", "n", "p", "qu", "r", "s", "t", "v", "y"]

        suffices = ["d", "h", "l", "n", "s"]

        # The core of the name is a randoma mount of consonant+vowel combinations.
        syllables = random.randint(2, 3)
        name = "".join([random.choice(consonants) + random.choice(vowels) for syllable in range(syllables)])

        # Add a prefix in the form of an extra vowel with a certain chance
        if random.randint(0, 1):
            name = random.choice(vowels) + name

        # Add a suffix in the form of a special extra consonant with a certain chance
        if random.randint(0, 1):
            name += random.choice(suffices)

        # Make the first letter uppercase
        name = name.title()

        return name
