import tkinter as tk 
import random as rand
import os


suits = ["♠", "♥", "♦", "♣"]
values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
deck = [(value, suit) for suit in suits for value in values]
hand = []

class PlayingCards:

    def __init__(self, deck, hand, card_quantity):
        self.deck = deck # Full deck of cards that the game draws from
        self.hand = hand # Players hand that they play with
        self.card_quantity = card_quantity # The number of cards that the player recieves
    

    def shuffle_deck(self):
        rand.shuffle(self.deck)
    

    def deal_cards(self):
        for i in range(self.card_quantity):
            card = self.deck.pop(0)
            self.hand.append(card)
        print(deck)
        print(hand)

os.system('cls' if os.name == 'nt' else 'clear')
print(deck)
print(hand)
testcards = PlayingCards(deck, hand, 2)
print() # gap
testcards.shuffle_deck()
print(deck)
print() # gap
testcards.deal_cards()