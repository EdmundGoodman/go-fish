#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from card_deck import Card, Faces, CardError
from os import system






class SafeInputs:
    @staticmethod
    def yes_no_input(prompt="Enter yes or no (y/n) "):
        """Repeatedly query for a yes or no input, until one is given, then
        return the appropriate boolean"""
        while True:
            out = str(input(prompt)).lower()
            if out == "y":
                return True
            elif out == "n":
                return False
            print("Enter either 'y' or 'n'")

    @staticmethod
    def enter_string_from_list(items, prompt, fail_prompt):
        """Given a list, repeatedly query until an item within in is given"""
        while True:
            string = str(input(prompt))
            if string in items:
                return string
            print(fail_prompt)

    @staticmethod
    def _general_cast_checker(prompt, fail_prompt, cast_function, cast_error):
        """Repeatedly take an input until one that can be cast to a provided
        type is given"""
        while True:
            try:
                return cast_function(input(prompt))
            except cast_error:
                print(fail_prompt)

    @staticmethod
    def int_input(prompt="Enter a number: "):
        """Ensure an integer is given without crashing on erroneous data"""
        return SafeInputs._general_cast_checker(
            prompt, "Enter a valid number",
            lambda x: int(x), ValueError
        )

    @staticmethod
    def face_input(prompt="Enter a card face: "):
        """Ensure an card face is given without crashing on erroneous data"""
        return SafeInputs._general_cast_checker(
            prompt, "Enter a valid face",
            lambda x: Card.get_face_from_typeable_name(str(x)), CardError
        )

    @staticmethod
    def card_input(prompt="Enter a card: "):
        """Ensure an card is given without crashing on erroneous data"""
        return SafeInputs._general_cast_checker(
            prompt, "Enter a valid card",
            lambda x: Card.get_from_typeable_name(str(x)), CardError
        )









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
    def __init__(self):
        """Initialise yourself as a player, entering your hand to the system"""
        super().__init__("Enter your name: ")
        hand_size = SafeInputs.int_input(
                                    "Enter the number of cards in your hand: ")
        # Enter your hand into the system, as you can see it

        # Start with both max and min at 0, not 4 and 0 respectively as we
        # know the values of all the cards
        self.face_ranges = {i:[0,0] for i in Faces}
        for i in range(hand_size):
            face = SafeInputs.face_input(
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
        num_players = SafeInputs.int_input(
                                "How many players (including you) are there: ")
        make_players = [You()]
        for i in range(1,num_players):
            make_players.append(Player("Enter player #{}'s name: ".format(i)))
        return make_players[0], {player.name:player for player in make_players}

    def show_table(self):
        """Show a tabulated version of the data being recorded"""
        width = max([len(player) for player in self.players]+[3]) + 2
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
                elif value == [4,4]:
                    # Pile known to be made
                    string = "#"
                elif value[0] == value[1]:
                    # If the number of cards held is known, don't print both
                    # minimum and maximum, as they are the same
                    string = str(value[0])
                else:
                    # Print any positive information on number of cards held
                    string = "-".join(map(str, value))
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
            # Display the collected information about the current game state
            system("clear")
            self.show_table()

            # Take the turn as an input
            player = SafeInputs.enter_string_from_list(
                self.players,
                "Enter the name of the current player: ",
                "Enter a valid player name"
            )
            if isinstance(self.players[player], You):
                card, person = self.suggested_move()
                #print("Try asking {} for a {}".format(person, card))

            target = SafeInputs.enter_string_from_list(
                self.players,
                "Enter the name of the player to ask: ",
                "Enter a valid player name"
            )
            face = SafeInputs.face_input("Enter the face guessed: ")

            # The target must either not have or proceed to lose all of the
            # cards of the guessed face
            self.players[target][face] = [0,0]

            if SafeInputs.yes_no_input("Was the guess correct (y/n) "):
                # The guess made was correct
                if SafeInputs.yes_no_input("Was a pile made (y/n) "):
                    # A pile was made, discarding the face from the game
                    self.piles[player] = face
                    for each_player in self.players.values():
                        each_player[face] = [0,0]
                    self.players[player][face] = [4,4]
                else:
                    # A number of cards of that face were transferred
                    num_cards = SafeInputs.int_input(
                                            "How many cards were passed over: ")
                    # The player must have had one card of that face to ask,
                    # but only add it in if the presumed minimum before was
                    # zero, as that could overflow the structure
                    player_obj = self.players[player]
                    offset = 1 if player_obj[face][0] == 0 else 0
                    flag = player_obj[face][0] == player_obj[face][1]
                    player_obj[face][0] += num_cards + offset
                    # If the value is already known, we want to increment the
                    # max (which is equal to the min) as well
                    if flag:
                        player_obj[face][1] = player_obj[face][0]
            else:
                # No cards were passed over, but the player must have had one
                # card of that face to ask, but only add it in if the presumed
                # minimum before was zero, as that could overflow the structure
                if self.players[player][face][0] == 0:
                    self.players[player][face][0] = 1

            # The max a player can have is the the total number of faces
            # subtract the minimum of all of the other players minimum
            # for that face, so update it each time a transfer is made
            sum_player_mins = sum([
                each_player[face][0] for each_player in self.players.values()
            ])
            for each_player in self.players.values():
                # Don't change maximums on players known to not have card
                if each_player[face][0] != each_player[face][1]:
                    each_player[face][1] = ((4 - sum_player_mins)
                                            + each_player[face][0])

            # If all other players have known cards, we can infer the number
            # of the final player
            for face in Faces:
                num_known_values, last_unknown_player = 0, None
                for each_player in self.players.values():
                    if each_player[face][0] == each_player[face][1]:
                        num_known_values += 1
                    else:
                        last_unknown_player = each_player
                if num_known_values == len(self.players)-1:
                    last_unknown_player[face][0] = last_unknown_player[face][1]


        # Show who won each pile
        self.show_piles()



if __name__ == "__main__":
    system("clear")
    g = Game()
    try:
        g.play()
    except KeyboardInterrupt:
        # If the program is ended, still show the piles accumulated up to this
        # point in case it doesn't end properly, and we go to round two :angry:
        # before the while loop breaks
        print()
        g.show_piles()
