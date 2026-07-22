import random as rand
import os

class PlayingCards:
    """Class for any card game. Creates, shuffles, and deals cards to the player."""
    def __init__(self):
        self.suits = ["♠", "♥", "♦", "♣"]
        self.values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.deck = [] # Full deck of cards that the game draws from
    

    def build_deck(self):
        # Creates a new deck at the start of each game. Make sure to clear the deck and hand first.
        for suit in self.suits:
            for value in self.values:
                self.deck.append((suit, value))



    def shuffle_deck(self):
        # Randomises the order of the cards before dealing
        rand.shuffle(self.deck)
    

    def deal_cards(self, card_quantity):
        # Deals a certain amount of cards and returns them as a list.
        # Put an integer as the argument to deal that many cards
        # In the game code, type: [hand var].extend([game var].deal_cards([num]))
        dealt = [] # stores the cards that are going to be given.
        if self.cards_remaining() < card_quantity:

            # Makes sure there is cards remaining in the deck
            raise ValueError("Not enough cards left in the deck!")
        
        for i in range(card_quantity):
            dealt.append(self.deck.pop())
        
        return dealt


    def clear_deck(self):
        self.deck.clear() # Resets deck for the new game
    

    def reset_cards(self):
        self.clear_deck()
        self.clear_hand()


    def cards_remaining(self):
        return len(self.deck)
    


# TESTING
os.system('cls' if os.name == 'nt' else 'clear')
blackjack = PlayingCards()
blackjack.build_deck()
blackjack.shuffle_deck()

player_hand = []
dealer_hand = []

player_hand.extend(blackjack.deal_cards(2))
dealer_hand.extend(blackjack.deal_cards(2))

print(player_hand)
print(dealer_hand)


