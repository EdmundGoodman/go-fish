from cardModel.cards import *



class Player:
    def __init__(self, name):
        self.name = name
        self._cardsHeld = set()
        self._cardsNotHeld = set()
        self._facesHeld = set()
        self._setsWon = set()

    def give(self, card):
        if card in self._cardsHeld:
            self._cardHeld.remove(card)
            self._cardsNotHeld.add(card)
            return card
        else:
            return None

    def ask(self, cardAsked, player):
        card = player.ask(cardAsked)
        if card is not None:
            self._cardsHeld.add(card)
            if card in self._cardsNotHeld:
                self._cardsNotHeld.remove(card)
            self._facesHeld.add(card.face) #Implicitly true, but ignore this
            #Handle set removal
        else:
            self._cardsNotHeld.add(cardAsked)
            self._facesHeld.add(cardAsked.face)

    def getSetsInUsableHand(self):
        justFaces = [card.face for card in self._cardsHeld]
        return [faces for faces in set(justFaces) if justFaces.count(faces) == 4]

        """for faceOfSet in facesOfSets:
            #Do this for all players!!!!
            self._setsWon.add(faceOfSet)
            self._facesHeld.remove
            for suit in Suits:
                self._cardsHeld.add()"""

    def __str__(self):
        out =  "{}:\n".format(self.name)
        out += "\tHolds the cards: {}\n".format(self._cardsHeld)
        out += "\tDoesn't hold the cards: {}\n".format(self._cardsNotHeld)
        out += "\tHolds the faces: {}\n".format(", ".join([face.name for face
                                                 in self._facesHeld]))
        out += "\tHas won the sets: {}\n".format(", ".join([face.name for face
                                                  in self._setsWon]))
        return out


    def __repr__(self):
        return str(self)

class You(Player):
    def __init__(self, cards=[]):
        super().__init__("You")
        self._cardsHeld.update(set(cards))
        self._cardsNotHeld.update(set(Deck() - Pile(cards)))
        self._facesHeld = set([card.face for card in cards])



class Game:
    def __init__(self):
        self.cardsInHand = 3
        self.players = []


if __name__=="__main__":
    p = Player("Edmund")
    p._cardsHeld.update(set([
        Card(Faces.ACE, Suits.HEARTS),
        Card(Faces.ACE, Suits.SPADES),
    ]))
    p._cardsNotHeld.update(set([
        Card(Faces.FIVE, Suits.HEARTS),
        Card(Faces.SIX, Suits.SPADES),
    ]))
    p._facesHeld.update(set([
        Faces.EIGHT
    ]))
    p._setsWon.update(set([
        Faces.NINE
    ]))
    print(p)
