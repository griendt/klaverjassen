import models.deck

if __name__ == "__main__":
    deck: models.deck.Deck = models.deck.Deck()

    print(deck)

    deck.shuffle()

    print(deck)
