import tkinter as tk 
import random as rand
import os

class PlayingCards:

    def __init__(self, card_quantity):
        self.suits = ["♠", "♥", "♦", "♣"]
        self.values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.deck = [] # Full deck of cards that the game draws from
        self.hand = [] # Players hand that they play with
        self.card_quantity = card_quantity # The number of cards that the player recieves
    

    def build_deck(self):
        for suit in self.suits:
            for value in self.values:
                self.deck.append((suit, value))

        print("- Before Shuffling & Dealing - ")
        print("deck:", self.deck)
        print("hand:", self.hand)


    def shuffle_deck(self):
        rand.shuffle(self.deck)

        print("- After Shuffling - ")
        print("deck:", self.deck)
        print("hand:", self.hand)
    

    def deal_cards(self):
        for i in range(self.card_quantity):
            card = self.deck.pop(0)
            self.hand.append(card)

        print("- After Dealing - ")
        print("deck:", self.deck)
        print("hand:", self.hand)


# TESTING
os.system('cls' if os.name == 'nt' else 'clear')
testcards = PlayingCards(2)
testcards.build_deck()
testcards.shuffle_deck()
testcards.deal_cards()
