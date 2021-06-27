#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from card_deck import Card, Faces, CardError

class Player:
    def __init__(self, name_prompt="Enter the player's name: "):
        """Initialise a player"""
        self.name = str(input(name_prompt))
        # Each player has a dictionary of card faces indexing 2-tuples of
        # the minimum and maximum possible number of that face they can hold in
        # their hand
        self.face_ranges = {i:[0,3] for i in Faces}

    def __iter__(self):
        """Create an iterator for the face ranges"""
        for face_range in self.face_ranges:
            yield face_range

    def __getitem__(self, face):
        """Get the card range for a given face"""
        return self.face_ranges[face]

    def __setitem__(self, face, face_range):
        """Set the card range for a given face"""
        self.face_ranges[face] = face_range

    def __repr__(self):
        """Display the players name as its string representation"""
        return self.name

class You(Player):
    def __init__(self, hand_size):
        """Initialise yourself as a player, entering your hand to the system"""
        super().__init__("Enter your name: ")
        # Enter your hand into the system, as you can see it

        # Start with both max and min at 0, not 4 and 0 respectively as we
        # know the values of all the cards
        self.face_ranges = {i:[0,0] for i in Faces}
        for i in range(hand_size):
            face = Game._enter_face(
                    "Enter the letter of face #{} in your hand: ".format(i+1))
            self.face_ranges[face][0] += 1
            self.face_ranges[face][1] += 1
        print("Your hand is: {}".format(self.show_hand()))

    def show_hand(self):
        """Display your hand"""
        hand = "{"
        leading_comma = ""
        for face,face_range in self.face_ranges.items():
            num_cards = face_range[0]
            if num_cards != 0:
                hand += leading_comma
                hand += ",".join([Card.LOOKUP_FACE_CHAR[face]] * num_cards)
                leading_comma = ","
        return hand + "}"


class Game:
    def __init__(self):
        """Initialise the game"""
        self.you, self.players = self.get_players()
        self.piles = {}

    def get_players(self):
        """Form a data structure containing the players"""
        hand_size = int(input("Enter the number of cards in your hand: "))
        make_players = [You(hand_size)]
        while True:
            make_players.append(Player())
            if Game._enter_yes_no("Have all the players been added (y/n) "):
                break
        return make_players[0], {player.name:player for player in make_players}

    def _enter_player_name(self, prompt):
        """Repeatedly prompt for the name of a player until one is entered"""
        while True:
            player_name = str(input(prompt))
            if player_name in self.players:
                break
            print("Please enter a valid player name")
        return player_name

    @staticmethod
    def _enter_face(prompt):
        """Repeatedly prompt for the typeable letter name of face until one
        is entered"""
        while True:
            #TODO: Remove this in next release of card_deck
            name = str(input(prompt)).upper()
            try:
                return Card.get_face_from_typeable_name(name)
            except CardError:
                print("Please enter a valid face: ")

    @staticmethod
    def _enter_yes_no(prompt):
        """Take a string and convert it to a boolean by repeatedly prompting
        until either the character 'y' or 'n' respectively is entered"""
        while True:
            out = str(input(prompt)).lower()
            if out == "y":
                return True
            elif out == "n":
                return False
            print("Please enter either 'y' or 'n'")

    def show_table(self):
        """Show a tabulated version of the data being recorded"""
        width = max([len(player) for player in self.players]) + 2
        horizontal_bar = "+-----+" + ("-"*width+"+")*len(self.players)

        # Print the header with the names in
        print(horizontal_bar)
        print("|     ", end="|")
        for player in self.players:
            print(player.center(width), end="|")
        print("\n"+horizontal_bar)

        # Print the data about each face for each player
        for face in Faces:
            print("|{}".format(Card.LOOKUP_FACE_CHAR[face].center(5)), end="|")
            for player_range in self.players.values():
                value = player_range[face]
                if value == [0,0]:
                    # Card known to be absent
                    string = "-"
                elif value == [-1,-1]:
                    # Pile known to be made
                    string = "#"
                elif value[0] == 0:
                    # No information on how many cards held
                    string = " "
                else:
                    # Positive information on minimum cards held
                    string = str(value[0]) #" - ".join(map(str, value))
                print(string.center(width), end="|")
            print()
        print(horizontal_bar)


    def show_piles(self):
        """Show the final piles accrued by each player over the game"""
        for player in self.players:
            if player in self.piles:
                print("{} has the piles: {}".format(player, self.piles[player]))
            else:
                print("{} has no piles".format(player))

    def suggested_move(self):
        """Suggest a move to play for the player stored at `self.you`"""
        return "face", "anyone"


    def play(self):
        """Play the game until it is over, tracking over player's moves, and
        suggesting ones for you"""

        while len(self.piles) < 12:
            self.show_table()

            player = self._enter_player_name(
                                    "Enter the name of the current player: ")

            if isinstance(self.players[player], You):
                card, person = self.suggested_move()
                #print("Try asking {} for a {}".format(person, card))

            # Take the turn as an input
            target = self._enter_player_name(
                                    "Enter the name of the player to ask: ")
            face = Game._enter_face("Enter the face guessed: ")

            # The target must either not have or proceed to lose all of the
            # cards of the guessed face
            self.players[target][face] = [0,0]

            if Game._enter_yes_no("Was the guess correct (y/n) "):
                # The guess made was correct
                if Game._enter_yes_no("Was a pile made (y/n) "):
                    # A pile was made, discarding the face from the game
                    self.piles[player] = face
                    for each_player in self.players:
                        self.players[each_player][face] = [-1,-1]
                else:
                    # A number of cards of that face were transferred
                    num_cards = int(input("How many cards were passed over: "))
                    offset = 0
                    if self.players[player][face][0] == 0:
                        # The player must have had one card of that face to ask,
                        # but only add it in if the presumed minimum before was
                        # zero, as that could overflow the structure
                        offset = 1
                    self.players[player][face][0] += num_cards + offset
            else:
                # No cards were passed over, but the player must have had one
                # card of that face to ask, but only add it in if the presumed
                # minimum before was zero, as that could overflow the structure
                if self.players[player][face][0] == 0:
                    self.players[player][face][0] = 1


        # Show who won each pile
        self.show_piles()



if __name__ == "__main__":
    g = Game()
    g.play()
