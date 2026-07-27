import random as rand
import os


class PlayingCards:
    """Class for any card game. Creates, shuffles, and deals cards to the player."""
    def __init__(self, deck_count=1):
        self.suits = ["♠", "♥", "♦", "♣"]
        self.values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
        self.deck = [] # Full deck of cards that the game draws from
        self.deck_count = deck_count
    

    def build_deck(self):
        # Creates a new deck at the start of each game.
        self.clear_deck()

        for i in range(self.deck_count):
            for suit in self.suits:
                for value in self.values:
                    self.deck.append((value, suit))



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
    

    def cards_remaining(self):
        return len(self.deck)
    

class BlackJack:

    def __init__(self):
        self.deck = PlayingCards()
        self.deck.build_deck()
        self.deck.shuffle_deck()

        self.player_hand = []
        self.dealer_hand = []

        self.game_over = False


    def hand_value(self, hand):
        total = 0
        aces = 0

        for value, suit in hand:
            if value in ["J", "Q", "K"]:
                total += 10
        
            elif value == "A":
                total += 11
                aces += 1
            
            else:
                total += int(value)
        
        while total > 21 and aces:
            total -= 10
            aces -= 1
        
        return total
    
    def deal_start(self):
        self.player_hand.extend(self.deck.deal_cards(2))
        self.dealer_hand.extend(self.deck.deal_cards(2))

    
    def hit(self):
        self.player_hand.extend(self.deck.deal_cards(1))

        if self.hand_value(self.player_hand) > 21:
            self.game_over = True

    
    def dealer_turn(self):
        while self.hand_value(self.dealer_hand) < 17:
            self.dealer_hand.extend(self.deck.deal_cards(1))
    

    def find_winner(self):
        player = self.hand_value(self.player_hand)
        dealer = self.hand_value(self.dealer_hand)

        if player > 21:
            return "Dealer"

        elif dealer > 21:
            return "Player"
        
        elif player > dealer:
            return "Player"
        
        elif dealer > player:
            return "Dealer"
        
        return "Draw"
    

    def show_hands(self, reveal=False):
        print("\nDealer:")

        if reveal:
            for card in self.dealer_hand:
                print(f"{card[0]}{card[1]}", end=" ")
            print(f" ({self.hand_value(self.dealer_hand)})")

        else:
            print(f"{self.dealer_hand[0][0]}{self.dealer_hand[0][1]} ?")

        print("\nPlayer:")

        for card in self.player_hand:
            print(f"{card[0]}{card[1]}", end=" ")

        print(f" ({self.hand_value(self.player_hand)})")


    def play_blackjack(self):
        self.deal_start()

        while not self.game_over:
            self.show_hands()

            choice = input("Hit or Stand? (h/s): ").lower()

            if choice == "h":
                self.hit()

            elif choice == "s":
                break
        
        if self.hand_value(self.player_hand) <= 21:
            self.dealer_turn()
        
        self.show_hands(True)

        print(f"\nWinner: {self.find_winner()}")


game = BlackJack()
game.play_blackjack()