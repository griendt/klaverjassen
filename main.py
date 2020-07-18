import models

if __name__ == "__main__":
    deck: models.Deck = models.Deck()

    print(deck)

    deck.shuffle()

    print(deck)
