from cardModel.cards import Suits, Faces, Card, Pile, Deck


class Player:
    def __init__(self, name):
        self.name = name
        self._cardsHeld = set()
        self._cardsNotHeld = set()
        self._setsWon = set()
        self._facesHeld = set()
        self._maxCardsForFace = {face:3 for face in Faces}
        #self._minCardsForFace = {face:0 for face in Faces}

    
    def give(self, card):
        if card is not None:
            #The player no longer holds the card
            self._cardHeld.remove(card)
            #The player doesn't hold the card
            self._cardsNotHeld.add(card)
            maxCardsForFace = self._maxCardsForFace[card.face]
            if maxCardsForFace > 0:
                #The player holds at least one fewer cards of that face than
                #the maximum they could have started with
                self._maxCardsForFace[card.face] -= 1
            if maxCardsForFace == 0 and card.face in self._facesHeld:
                #If the player has given away all cards of a face from the
                #maximum they could have started with, they must not hold any of
                #that face anymore
                self._facesHeld.remove(card.face)

    def ask(self, card, received, otherPlayers):
        if received:
            self._cardsHeld.add(card)
            self._facesHeld.add(card.face)
            if self._maxCardsForFace < 3:
                self._maxCardsForFace += 1
            

        else:
            #The player cannot hold a card they just asked for, and they
            #didn't receive, so they don't hold it now
            self._cardsNotHeld.add(card)
            #The player must hold at least one card of that face to have asked
            #for that card
            self._facesHeld.add(card.face)

            if self._maxCardsForFace == 0:
                #If we have tracked them to not have any cards of this face,
                #complain about it
                print("The program has tracked them losing all cards of that")
                print("face. Please check if they have made a mistake")
