from models.card import Deck

if __name__ == "__main__":
    deck: Deck = Deck()

    print(deck)

    deck.shuffle()

    print(deck)