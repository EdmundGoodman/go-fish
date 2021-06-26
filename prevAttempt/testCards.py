from cardModel.cards import *

if __name__=="__main__":
    """Test the interfaces of the objects"""
    import copy

    #Test getting the typeable name of a card
    print(Card(Faces.SIX, Suits.SPADES).getTypeableName())

    #Test gettting a card form its typeable name
    while True:
        inp = str(input("Enter the typeable name of a card: "))
        card = CardFromTypeableName().getCard(inp)
        if card is not None:
            break
    print(card)



    #Test making Decks and Pile
    d1 = Deck()
    d2 = Pile([Card(Faces.ACE, Suits.DIAMONDS)])
    d3 = Pile([
        Card(Faces.ACE, Suits.HEARTS),
        Card(Faces.FIVE, Suits.CLUBS),
    ])

    #Test operations on Decks and Piles
    print(dir(d1))
    print(Card.__doc__(Card))
    print(d1)
    print(d2)
    print(d1-d2)
    print(d1 ^ d2)
    print(d1 and d3)
    print(d1 is copy.deepcopy(d1))

    #Test the hash functions of Pile objects
    print(hash(d1))
    print(hash(d2))
