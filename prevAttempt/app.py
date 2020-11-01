import enum
import random

from cards import *



class Player:
    def __init__(self, name, numCards):
        self.name = name
        self.numCards = numCards
        self.cardsHeld = set()
        self.cardsNotHeld = set()
        self.facesHeld = set() #Faces DEFINITELY held - removed if card is taken
        self.setsHeld = set()

    def addCardHeld(self, card):
        self.cardsHeld.add(card)
        self.handleSets(card)

    def handleSets(self, card):
        face = card.getFace()
        setCards = set()
        for suit in Suits:
            newCard = Card(suit, face)
            if newCard not in self.cardsHeld:
                break
            else:
                setCards.add(newCard)
        if len(cards):
            self.setsHeld.add(setCards)
            self.removeFaceHeld(face)
            for setCard in setCards:
                self.removeCardHeld(setCards)

    def removeCardHeld(self, card):
        if card in self.cardsHeld:
            self.cardsHeld.remove(card)

    def addCardNotHeld(self, card):
        self.cardsNotHeld.add(card)

    def removeCardNotHeld(self, card):
        if card in self.cardsNotHeld:
            self.cardsNotHeld.remove(card)

    def addFaceHeld(self, face):
        self.facesHeld.add(face)

    def removeFaceHeld(self, face):
        if face in self.facesHeld:
            self.facesHeld.remove(face)

    """def getHeldSets(self):
        heldSets = set()
        for face in Faces:
            flag = True
            for suit in Suits:
                if Card(suit, face) not in self.cardsHeld:
                    flag = False
                    break
            if flag:
                heldSets.add(face)
        return heldSets"""


    def __repr__(self):
        string = "Player {}:".format(self.name)
        string += "\n\tHas: {}".format(
            ", ".join([str(x) for x in self.cardsHeld]) if len(self.cardsHeld) != 0 else "-"
        )
        if self.name == You.NAME:
            string += "\n\tDoesn't have: {...}"
        else:
            string += "\n\tDoesn't have: {}".format(
                ", ".join([str(x) for x in self.cardsNotHeld]) if len(self.cardsHeld) != 0 else "-"
            )
        string += "\n\tHas cards with the faces: {}".format(
            ", ".join([x.name for x in self.facesHeld]) if len(self.cardsHeld) != 0 else "-"
        )
        string += "\n\tHas the sets: {}".format(
            ", ".join([x.name for x in self.setsHeld]) if len(self.cardsHeld) != 0 else "-"
        )

        return string



class You(Player):
    NAME = "You"
    def __init__(self, numCards, cards):
        Player.__init__(self, You.NAME, numCards)
        self.cardsHeld = set(cards)
        self.cardsNotHeld = set([card for card in Deck().get()
                                if card not in self.cardsHeld])
        for card in self.cardsHeld:
            self.addFaceHeld(card.getFace())



class Game:
    def __init__(self, numPlayers, numCards):
        self.deck = Deck()
        self.players = []
        self.numPlayers = numPlayers
        self.numCards = numCards


    def start(self):
        self.initialisePlayers()
        print()

        while True:
            for player in self.players:
                print("{}'s turn: ".format(player.name))
                print(player)
                print()

                if player.name == You.NAME:
                    ### Do a print out about other players states
                    for playerToPrint in self.players:
                        print(player)
                        print()
                    print()

                    ### Point out if you know the positions of all the other cards of a face
                    moveSuggested = False

                    for face in Faces:
                        facesKnown = {}
                        for playerFace in players:
                            for card in playerFace.cardsHeld:
                                if card.getFace() == face:
                                    facesKnown[card] = playerFace
                        if len(facesKnown) == 4:
                            moveSuggested = True
                            print("\nAll four cards of the face {} are known!".format(face))
                            for key,value in facesKnown:
                                print("{} has {}".format(value, key))

                    ### Suggest taking a card which you have fewest? of
                    if not moveSuggested:
                        print("No especially good moves exist, consider asking for a card from a face you have few of?")

                #Take input about the game state
                asker = player
                asked = self.getPlayerByName("\tEnter the target player's name: ")

                card = self.getCard("\tEnter the card was asked for: ")
                correct = self.getYesNo("\tEnter if the request was correct (y/n): ")

                #The asked face is held by the asker
                asker.addFaceHeld(card.getFace())
                if correct:
                    #The asker has the asked card
                    #   - the asker now has that card, and don't not have it
                    #   - the asked now doesn't have that card, and does not have it
                    #   - the asked doesn't necessarily have any cards of that face left
                    asker.addCardHeld(card)
                    asker.removeCardNotHeld(card)
                    asked.addCardNotHeld(card)
                    asked.removeCardHeld(card)
                    asked.removeFaceHeld(card.face)
                else:
                    #The card is held neither by the asker nor the asked
                    #   - the asker doesn't have that card
                    #   - the asked doesn't have that card
                    asker.addCardNotHeld(card)
                    asked.addCardNotHeld(card)

                print(player)
                print()
                print()


    def initialisePlayers(self):
        """Enter your cards and position, then initialise all the players
        in the data structures"""
        #Enter your cards and your position in the course of play
        yourCards = self.getYourCards()
        yourPosition = self.getYourPosition()

        #Create players in order of the course of play, indcluding you
        for i in range(self.numPlayers):
            if i == yourPosition-1:
                self.players.append(You(self.numCards, yourCards))
            else:
                playerName = input("Enter player {}'s name: ".format(i+1))
                self.players.append(Player(playerName, self.numCards))

    def getYourCards(self):
        """Get a list of the cards in your hand"""
        return [self.getCard("\tEnter one of your cards: ") for i in range(self.numCards)]

    def getCard(self, message="Enter a card: "):
        """Return a card object from an input of a specified format - first
        the first letter of the face, then the first letter of the suit, for
        example 'Jack of Spades' would be JS, and 'Two of Hearts' would be 2H"""
        while True:
            inp = input(message).upper()
            face, suit = inp[0], inp[1]
            if face in FacesInputLookup and suit in SuitsInputLookup:
                return Card(SuitsInputLookup.index(face),
                            FacesInputLookup.index(suit))
            else:
                print("Invalid card")

    def getYesNo(self, message):
        """Get a boolean selection from a yes or no answer to a message"""
        while True:
            correct = input(message).lower()
            if correct in ["y","n"]:
                return True if correct == "y" else False
            else:
                print("Invalid state")

    def getYourPosition(self):
        """Get the users position (i.e. first to play) in the game"""
        while True:
            position = input("Enter your position in the course of play: ")
            if position.isdigit() and 1 <= int(position) <= self.numPlayers:
                return int(position)
            else:
                print("Invalid position")

    def getPlayerByName(self, message="Enter the player's name: "):
        while True:
            name = input(message)
            for player in self.players:
                if player.name == name:
                    return player
            print("Invalid name")


if __name__=="__main__":
    numPlayers = int(input("Enter the number of people playing: "))
    numCards = int(input("Enter the number of cards dealt to each player: "))
    g = Game(numPlayers, numCards)
    g.start()
