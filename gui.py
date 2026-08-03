import tkinter as tk
import random as rand


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
    # Blackjack game code. Call this class to begin a game of blackjack
    def __init__(self):
        self.deck = PlayingCards()
        self.deck.build_deck()
        self.deck.shuffle_deck()

        self.player_hand = []
        self.dealer_hand = []

        self.game_over = False


    def hand_value(self, hand):
        # Finds the value of a specific hand.
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
        # Starts the game by giving the player and dealer 2 cards each
        self.player_hand.extend(self.deck.deal_cards(2))
        self.dealer_hand.extend(self.deck.deal_cards(2))

    
    def hit(self):
        # When player clicks the hit button, this function draws an extra card
        self.player_hand.extend(self.deck.deal_cards(1))

        if self.hand_value(self.player_hand) > 21:
            self.game_over = True

    
    def dealer_turn(self):
        # Computer program to run the dealers turn.
        while self.hand_value(self.dealer_hand) < 17:
            self.dealer_hand.extend(self.deck.deal_cards(1))
    

    def find_winner(self):
        # If loops that find the winner of each game
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
        # Displays the cards of the dealer and player hands. Will be changed when GUI is connected
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


    def play(self):
        # Game play function for blackjack
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


class CasinoGUI:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Red Clover Casino")
        self.root.geometry("800x600")

        # Function to load the frame header with the users balance etc.
        self.create_header()

        # Displays the page that the user is on
        self.content_frame = tk.Frame(self.root, bg="#1f1b1d")
        self.content_frame.pack(fill="both", expand=True)

        # Function to load the default page - will be changed to login page when I create it
        self.show_homepage()

    def clear_content(self):
        # Resets the frame before showing a new page
        for widget in self.content_frame.winfo_children(): # I used tutorialspoint.com to find this tkinter function
            widget.destroy()

    def create_header(self):
        self.header_frame = tk.Frame(self.root, bg="#d4142a")
        self.header_frame.pack(fill="both")

        self.header_frame.columnconfigure([0, 3], weight=2)
        self.header_frame.columnconfigure([1, 2], weight=3) # middle columns are slightly wider to allow room for title
        self.header_frame.rowconfigure(0, weight=1)

        self.username_label = tk.Label(self.header_frame, text="[username]", bg="#d4142a", fg="black", font="Arial 16 bold")
        self.username_label.grid(row=0, column=0, sticky="nsew", pady=8)

        self.title_label = tk.Label(self.header_frame, text="Red Clover Casino", bg="#d4142a", fg="black", font="Arial 28 bold")
        self.title_label.grid(row=0, column=1, columnspan=2, sticky="nsew", pady=8)

        self.balance_label = tk.Label(self.header_frame, text="$67.67", bg="#d4142a", fg="black", font="Arial 16 bold")
        self.balance_label.grid(row=0, column=3, sticky="nsew", pady=8)

    def show_homepage(self):
        # ----- HOME PAGE    -----

        self.homepage = tk.Frame(self.content_frame, bg="#1f1b1d")
        self.homepage.pack(fill="both", expand=True)

        self.homepage.rowconfigure(0, weight=1) # Header row
        self.homepage.rowconfigure([1, 2, 3, 4], weight=3)
        self.homepage.columnconfigure([0, 1, 2, 3], weight=1)

        # Button screen
        self.blackjack_button = tk.Button(self.homepage, text="BLACKJACK", bg="#d4142a", fg="black", font="Arial 22 bold", borderwidth=0, command=lambda: self.show_blackjack())
        self.blackjack_button.grid(row=1, column=0, columnspan=2, rowspan=2, padx=(32, 16), pady=(32, 16), sticky="nsew")

        self.slots_button = tk.Button(self.homepage, text="SLOTS", bg="#d4142a", fg="black", font="Arial 22 bold", borderwidth=0)
        self.slots_button.grid(row=1, column=2, columnspan=2, rowspan=2, padx=(16, 32), pady=(32, 16), sticky="nsew")

        self.highlow_button = tk.Button(self.homepage, text="HIGH/LOW", bg="#d4142a", fg="black", font="Arial 22 bold", borderwidth=0)
        self.highlow_button.grid(row=3, column=0, columnspan=2, rowspan=2, padx=(32, 16), pady=(16, 32), sticky="nsew")

        # Profile/Leaderboard container
        self.info_frame = tk.Frame(self.homepage, bg="#1f1b1d")
        self.info_frame.grid(row= 3, column=2, columnspan=2, rowspan=2, padx=(16, 32), pady=(16, 32), sticky="nsew")

        self.info_frame.rowconfigure([0, 1], weight=1)
        self.info_frame.columnconfigure(0, weight=1)

        self.leaderboard_button = tk.Button(self.info_frame, text="LEADERBOARD", bg="#d4142a", fg="black", font="Arial 22 bold", borderwidth=0)
        self.leaderboard_button.grid(row=0, column=0, pady=(0, 16), sticky="nsew")

        self.profile_button = tk.Button(self.info_frame, text="PROFILE", bg="#d4142a", fg="black", font="Arial 22 bold", borderwidth=0)
        self.profile_button.grid(row=1, column=0, pady=(16, 0), sticky="nsew")

    def show_blackjack(self):
        # Starts a new game
        self.clear_content()
        self.game = BlackJack()
        self.game.deal_start()

        # Green table (background for game)
        self.blackjack_screen = tk.Frame(self.content_frame, bg="#008000", highlightbackground="#d4142a", highlightthickness=6)

        self.blackjack_screen.pack(fill="both", expand=True, padx=64, pady=32)

        self.blackjack_screen.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7], weight=1)
        self.blackjack_screen.columnconfigure([0, 1, 2, 3, 4, 5, 6], weight=1)

        # Dealer cards
        self.dealer_frame = tk.Frame(self.blackjack_screen, bg="#008000")
        self.dealer_frame.grid(row=1, column=2, columnspan=3)

        # Dealer label
        self.dealer_total = tk.Label(self.blackjack_screen, text="Dealer", bg="#008000", font="Arial 18")
        self.dealer_total.grid(row=2, column=3)

        # Deck
        self.deck_card = self.create_card(self.blackjack_screen, hidden=True)
        self.deck_card.grid(row=2, column=0)

        # Player label
        self.player_total = tk.Label(self.blackjack_screen, text="You", bg="#008000", font="Arial 18")
        self.player_total.grid(row=4, column=3)

        # Player cards
        self.player_frame = tk.Frame(self.blackjack_screen, bg="#008000")
        self.player_frame.grid(row=5, column=1, columnspan=5)

        # Draw starting cards
        self.update_blackjack_gui()

        # Buttons
        self.create_blackjack_buttons()

        # Winner label
        self.result_label = tk.Label(self.content_frame, text="", bg="#1f1b1d", fg="white", font="Arial 18 bold")
        self.result_label.pack(pady=10)

    def create_card(self, parent, card=None, hidden=False):
        if hidden:
            background = "#9e0000"
            foreground = "white"
            text = "?"

        else:
            value, suit = card
            background = "white"
            foreground = "black"
            text = f"{value}\n{suit}"

        card_label = tk.Label(parent, text=text, bg=background, fg=foreground, width=4, height=3, relief="solid", borderwidth=2, font="Arial 18 bold")

        return card_label

    def update_blackjack_gui():
        # Updates screen when new card is drawn
        print("placeholder")


# Main program Function
def main():
    root = tk.Tk()
    app = CasinoGUI(root)
    root.mainloop()


# Runs Program
main()