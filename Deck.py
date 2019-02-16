import random
# ♥ - hearts
# ♦ - tiles
# ♣ - clovers
# ♠ - pikes

# J - jack
# Q - queen
# K - king
# A - ace


class Deck:
    CARDS = tuple([i + k for k in '♥♣♠♦' for i in '67890JQKA'])
    def __init__(self, cards=CARDS):
        self.deсk = list(cards)
        for i in range(random.randint(3, 9)):
            random.shuffle(self.deсk)

    def push(self, card):
        self.deсk.insert(0, card)

    def pull(self):
        return self.deck.pop()
