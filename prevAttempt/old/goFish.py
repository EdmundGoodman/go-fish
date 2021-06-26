import enum
import random

class Suits(enum.Enum):
    Diamonds = 1
    Clubs = 2
    Hearts = 3
    Spades = 4


class Faces(enum.Enum):
    Ace = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13

SuitsInputLookup = [data.name[0] for data in Suits] #FIXME: Maybe make these sets?
FacesInputLookup = [data.name[0] for data in Faces]


class Card:
    def __init__(self, suit, face):
        self.suit = suit
        self.face = face

    def getSuit(self):
        return self.suit

    def getFace(self):
        return self.face

    def __repr__(self):
        faceChars = "A,2,3,4,5,6,7,8,9,10,J,Q,K".split(",")
        suitChars = '♦,♣,♥,♠'.split(",")
        return faceChars[self.face.value-1] + suitChars[self.suit.value-1]


class Pile:
    def __init__(self, cards=[]):
        self.cards = cards #FIXME: This could be an ordered set not a list

    def shuffle(self):
        random.shuffle(self.cards)

    def get(self):
        return self.cards

    def remove(self, card):
        self.cards.remove(card)

    def pop(self):
        return self.cards.pop()

    def peek(self):
        return self.cards[-1]

    def place(self, card, position=None):
        if position is None:
            position = len(self.cards)
        self.cards.insert(position, card)

    def insert(self, card):
        self.place(card, random.randint(0, len(self.cards)))

    def deal(self, numSets, numCards):
        sets = [[] for n in range(numSets)]
        for i in range(numCards):
            for j in range(numSets):
                sets[j].append(self.pop())
        return sets

    def __repr__(self):
        return ", ".join([str(x) for x in self.cards])


class Deck(Pile):
    def __init__(self):
        Pile.__init__(self)
        for suit in Suits:
            for face in Faces:
                self.cards.append(Card(suit, face))


#===========================================================

class Player:
    def __init__(self, numCardsHeld):
        self.numCardsHeld = numCardsHeld
        self.cardsHeld = set() #FIXME: This could be a pile not a set
        self.cardsNotHeld = set()
        self.facesHeld = set()

    def addCardHeld(self, card):
        self.cardsHeld.add(card)
        self.facesHeld.add(card.getFace)

    def addCardsHeld(self, cards):
        for card in cards:
            self.cardsHeld.add(card)

    def addCardNotHeld(self, card):
        self.cardsNotHeld.add(card)

    def addFaceHeld(self, face):
        self.facesHeld.add(face)

    def getCardsHeld(self):
        return self.cardsHeld

    def getCardsNotHeld(self):
        return self.cardsNotHeld

    def getFacesHeld(self):
        return self.facesHeld

    def getNumCardsOfFace(self, face):
        count = 0
        for card in cardsHeld:
            if card.getFace == face:
                count += 1
        return count


class Game:
    def __init__(self, numPlayers, numCards):
        self.deck = Deck()
        self.players = [Player(numCards) for i in range(numPlayers)]
        self.numPlayers = numPlayers
        self.numCards = numCards

    def start(self):
        self.playerNames = self.getPlayerNames()
        self.yourNum = self.getPlayerNum("Enter your name: ")
        self.players[self.yourNum].addCardsHeld(self.getYourCards())

        run = () #player, face
        while True:
            asker = self.getPlayerNum("Enter the name of the current player: ")
            if asker == self.yourNum:
                #Output the suggested play

                #If you know someone has cards with faces you have, take them
                #Definitely if three, wait if they are known to have two and
                #you have one - account for fact people want duplicate Qs?
                for face in self.players[self.yourNum].getFacesHeld():
                    for player in self.players:
                        if player.getNumCardsOfFace(face) == 3:
                            #Take all their cards
                            pass

                #Output percentage likelihood of players having cards/most
                #likely hands?

            #Input the data about the play
            asked = self.getPlayerNum("Enter the name of the player asked: ")
            card = self.getCard("Enter the card asked for: ")
            correct = self.getQueryCorrectness()
            #Update the algorithm state

            #The asked face is held by the asker
            self.players[asker].addFaceHeld(card.getFace())
            if correct:
                #The asker has the asked card
                self.players[asker].addCardHeld(card)
            else:
                #The card is held neither by the asker nor the asked
                self.players[asker].addCardNotHeld(card)
                self.players[asked].addCardNotHeld(card)


    def getPlayerNames(self):
        playerNames = {}
        for i in range(self.numPlayers):
            playerNames[input("Enter player #{}'s name: ".format(i+1))] = i
        return playerNames

    def getPlayerNum(self, message):
        while True:
            inp = input(message)
            if inp in self.playerNames:
                return self.playerNames[inp]
            else:
                print("Invalid name")

    def getYourCards(self):
        return [getCard("Enter your card: ") for i in range(self.numCards)]

    def getCard(self, message):
        while True:
            #Format for entry is face letter, e.g. J for jack then suit
            #letter, e.g S for spades For example, to enter the ace of
            #hearts, type 'AH'
            inp = input(message).upper()
            if face in FacesInputLookup and suit in SuitsInputLookup:
                return Card(SuitsInputLookup.index(inp[0]),
                            FacesInputLookup.index(inp[1]))
            else:
                print("Invalid card")

    def getQueryCorrectness(self):
        while True:
            correct = input("Enter whether the query was correct (y/n): ").lower()
            if correct in ["y","n"]:
                return True if correct == "y" else False
            else:
                print("Invalid state")

if __name__=="__main__":
    numPlayers = int(input("Enter the number of people playing: "))
    numCards = int(input("Enter the number of cards dealt to each player: "))
    g = Game(numPlayers, numCards)
    g.start()
