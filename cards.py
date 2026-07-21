import tkinter as tk 
import random as rand
import os

class PlayingCards:
    """Class for any card game. Creates, shuffles, and deals cards to the player."""
    def __init__(self):
        self.suits = ["♠", "♥", "♦", "♣"]
        self.values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.deck = [] # Full deck of cards that the game draws from
        self.hand = [] # Players hand that they play with
    

    def build_deck(self):
        # Creates a new deck at the start of each game. Make sure to clear the deck and hand first.
        for suit in self.suits:
            for value in self.values:
                self.deck.append((suit, value))

        print("- Before Shuffling & Dealing - ")
        print("deck:", self.deck)
        print("hand:", self.hand)


    def shuffle_deck(self):
        # Randomises the order of the cards before dealing
        rand.shuffle(self.deck)

        print("- After Shuffling - ")
        print("deck:", self.deck)
        print("hand:", self.hand)
    

    def deal_cards(self, card_quantity):
        # Gives a certain amount of cards to the player
        # Put an integer as the argument to deal that many cards
        for i in range(card_quantity):
            card = self.deck.pop(0)
            self.hand.append(card)

        print("- After Dealing - ")
        print("deck:", self.deck)
        print("hand:", self.hand)


    def clear_deck(self):
        self.deck.clear() # Resets deck for the new game
    

    def clear_hand(self):
        self.hand.clear() # Wipes hand for the new game
    

    def reset_cards(self):
        self.clear_deck()
        self.clear_hand()
        print("deck:", self.deck)
        print("hand:", self.hand)
    


# TESTING
os.system('cls' if os.name == 'nt' else 'clear')
testcards = PlayingCards()
testcards.build_deck()
testcards.shuffle_deck()
testcards.deal_cards(2)
testcards.deal_cards(1)
testcards.clear_deck()
testcards.build_deck()
testcards.reset_cards()
