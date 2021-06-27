#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from card_deck import Card, Faces, Suits, Deck, CardError, PileError




class SafeInputs:
    @staticmethod
    def yes_no_input(prompt="Enter 'y' or 'n': "):
        while True:
            out = str(input(prompt)).lower()
            if out == "y":
                return True
            elif out == "n":
                return False
            print("Enter either 'y' or 'n'")

    @staticmethod
    def enter_string_from_list(items, prompt, fail_prompt):
        while True:
            string = str(input(prompt))
            if string in items:
                return string
            print(fail_prompt)

    @staticmethod
    def _general_cast_checker(prompt, fail_prompt, cast_function, cast_error):
        while True:
            try:
                return cast_function(input(prompt))
            except cast_error:
                print(fail_prompt)

    @staticmethod
    def int_input(prompt="Enter a number: "):
        return SafeInputs._general_cast_checker(
            prompt, "Enter a valid number",
            lambda x: int(x), ValueError
        )

    @staticmethod
    def face_input(prompt="Enter a card face: "):
        return SafeInputs._general_cast_checker(
            prompt, "Enter a valid face",
            lambda x: Card.get_face_from_typeable_name(str(x)), CardError
        )

    @staticmethod
    def card_input(prompt="Enter a card: "):
        return SafeInputs._general_cast_checker(
            prompt, "Enter a valid card",
            lambda x: Card.get_from_typeable_name(str(x)), CardError
        )






class Player:
    def __init__(self, cards, num_players, prompt="Enter the player's name"):
        self.name = str(input(prompt))
        self.hand_size = SafeInputs.int_input(
                                "Enter the number of cards in your hand")
        # Make a dictionary of probabilities of the cards being held
        self.probabilities = {}
        for card in Deck():
            if card in cards:
                self.probabilities[card] = 1/num_players
            else:
                self.probabilities[card] = 0

    def __repr__(self):
        return self.name

class You(Player):
    def __init__(self, cards, num_players):
        super().__init__(cards, num_players, "Enter your name: ")
        # Remove cards known to be held from the list of unknown cards
        for i in range(self.hand_size):
            card = SafeInputs.card_input(
                    "Enter the letter of card #{} in your hand: ".format(i+1))
            cards.remove(card)
        # Make a dictionary of probabilities of the cards being held
        for card in Deck():
            if card not in cards:
                self.probabilities[card] = 1





class Game:
    def __init__(self):
        self.unknown_cards = Deck()
        self.players = self.get_players()
        self.piles = {}

    def get_players(self):
        """Form a data structure containing the players"""
        #Pass by reference on lists should mutate it
        num_players = SafeInputs.int_input("How many players are there: ")

        you = You(self.unknown_cards, num_players)
        players = {str(you):you}

        while True:
            player = Player(self.unknown_cards, num_players)
            players[str(player)] = player


    def play(self):
        while len(self.piles) < 12:

            player = SafeInputs.enter_string_from_list(
                self.players,
                "Enter the name of the current player: ",
                "Enter a valid player name"
            )
            target = SafeInputs.enter_string_from_list(
                self.players,
                "Enter the name of the player to ask: ",
                "Enter a valid player name"
            )
            face = SafeInputs._enter_face("Enter the face guessed: ")


            for suit in Suits:
                card = Card(face, suit)
                self.players[target].probabilities[card] = 0

            if SafeInputs.yes_no_input("Was the guess correct (y/n) "):
                # The guess made was correct
                if Game._enter_yes_no("Was a pile made (y/n) "):
            else:
                

if __name__ == "__main__":
    g = Game()
    g.play()
