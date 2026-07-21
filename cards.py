import tkinter as tk 
import random as rand
import os


suits = ["♠", "♥", "♦", "♣"]
values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
deck = []
hand = []

class PlayingCards:

    def __init__(self, deck, hand, card_quantity):
        self.suits = suits 
        self.values = values
        self.deck = deck # Full deck of cards that the game draws from
        self.hand = hand # Players hand that they play with
        self.card_quantity = card_quantity # The number of cards that the player recieves
    

    def build_deck(self):
        for suit in suits:
            for value in values:
                deck.append((suit, value))


    def shuffle_deck(self):
        rand.shuffle(self.deck)
    

    def deal_cards(self):
        for i in range(self.card_quantity):
            card = self.deck.pop(0)
            self.hand.append(card)


# TESTING
os.system('cls' if os.name == 'nt' else 'clear')
testcards = PlayingCards(deck, hand, 2)
testcards.build_deck()
print("- Before Shuffling & Dealing - ")
print("deck:", deck)
print("hand:", hand)
print() # gap
testcards.shuffle_deck()
print("- After Shuffling - ")
print("deck:", deck)
print() # gap
testcards.deal_cards()
print("- After Dealing - ")
print("deck:", deck)
print("hand:", hand)