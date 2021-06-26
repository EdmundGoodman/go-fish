import enum
import random

import copy


class Suits(enum.Enum):
    DIAMONDS = 1
    CLUBS = 2
    HEARTS = 3
    SPADES = 4



class Faces(enum.Enum):
    ACE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13


SuitsInputLookup = [data.name[0] for data in Suits]
FacesInputLookup = [data.name[0] for data in Faces]


class Card:
    def __init__(self, suit, face):
        self.suit = suit
        self.face = face

    def getSuit(self):
        return self.suit

    def getFace(self):
        return self.face

    #https://web.archive.org/web/20110131211638/http://diveintopython3.org/special-method-names.html

    def __eq__(self, other):
        return self.suit == other.suit and self.face == other.face

    def __ne__(self, other):
        return self == other

    def __lt__(self, other):
        if self.face < other.face:
            return True
        else:
            return self.suit < other.suit

    def __le__(self, other):
        return self < other or self == other

    def __gt__(self, other):
        if self.face > other.face:
            return True
        else:
            return self.suit > other.suit

    def __ge__(self, other):
        return self > other or self == other

    def __hash__(self):
        return int(str(self.suit.value)+str(self.face.value))

    def __str__(self):
        faceChars = "A,2,3,4,5,6,7,8,9,10,J,Q,K".split(",")
        suitChars = '♦,♣,♥,♠'.split(",")
        return faceChars[self.face.value-1] + suitChars[self.suit.value-1]

    def __repr__(self):
        return str(self)



class Pile:
    def __init__(self, cards=[]):
        self.cards = cards

    def get(self):
        return self.cards

    def pop(self, position=None):
        if position is None:
            position = len(self.cards) - 1
        return self.cards.pop()

    def peek(self, position=-1):
        return self.cards[position]

    def place(self, card, position=None):
        if position is None:
            position = len(self.cards)
        self.cards.insert(position, card)

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, numSets, numCards):
        sets = [[] for n in range(numSets)]
        for i in range(numCards):
            for j in range(numSets):
                sets[j].append(self.pop())
        return sets

    def __add__(self, other):
        return Pile( self.cards.extend(other.cards) )

    def __sub__(self, other):
        return Pile( [item for item in self if item not in other] )

    def __iter__(self):
        for card in self.cards:
            yield card

    def __contains__(self, item):
        return item in self.get()

    def __len__(self):
        return len(self.cards)

    def __and__(self, other):
        return [item for item in self.cards if item in other.cards]

    def __or__(self, other):
        return list( set(self.cards).union(set(other.cards)) )

    def __eq__(self, other):
        return self.cards == other.cards

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return int("".join([str(hash(x)) for x in self.cards]))

    def __str__(self):
        return ", ".join([str(x) for x in self.cards])

    def __repr__(self):
        return str(self)



class Deck(Pile):
    def __init__(self):
        Pile.__init__(self)
        for suit in Suits:
            for face in Faces:
                self.cards.append(Card(suit, face))



if __name__=="__main__":
    """Test the interfaces of the objects"""

    d1 = Deck()
    d2 = Pile([Card(Suits.DIAMONDS, Faces.ACE)])
    d3 = Pile([
        Card(Suits.DIAMONDS, Faces.ACE),
        Card(Suits.CLUBS, Faces.FIVE),
    ])

    print(d1)
    print(d2)
    print(d1-d2)
    print(d1 and d3)
    print(d1 is copy.deepcopy(d1))
    print(hash(d1))
    print(hash(d2))
