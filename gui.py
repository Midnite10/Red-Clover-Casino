import tkinter as tk
from tkinter import messagebox
import random as rand
import json
import os

class Constants:
    # ----- General -----
    CASINO_NAME = "Red Clover Casino"
    WINDOW_SIZE = "800x600"

    # ----- Colours -----
    BG_COLOUR = "#1f1b1d" # Background colour
    MAIN_COLOUR = "#d4142a" # Main red colour
    TABLE_COLOUR = "#008000" # For blackjack table
    CARD_BACK_COLOUR = "#9e0000" # The back of the card
    CARD_FRONT_COLOUR = "white" # The front of the card
    WHITE = "white" # can change to a different shade of white if needed

    # ----- Fonts -----
    TITLE_FONT = "Arial 28 bold"
    LG_FONT = "Arial 22 bold"
    MD_FONT = "Arial 18 bold"
    SM_FONT = "Arial 14"
    SM_FONT_BOLD = "Arial 14 bold"

    # ----- Accounts -----
    STARTING_BALANCE = 1000
    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 16
    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 32


class Accounts:
    # Manages the accounts system for the casino
    def __init__(self):
        folder = os.path.dirname(os.path.abspath(__file__)) # Found from geeksforgeeks.org. Only used to make sure the file is in the right place so that you can view it easily
        self.filename = os.path.join(folder, "accounts.json") # json file containing all accounts

    def load_accounts(self):
        # loads accounts onto program
        try:
            with open(self.filename, "r") as file:
                return json.load(file)

        except (FileNotFoundError, json.JSONDecodeError): # if file isn't found
            return {}
    
    def save_accounts(self, accounts):
        print(os.getcwd())
        # saves accounts info to json file
        with open(self.filename, "w") as file:
            json.dump(accounts, file, indent=4)
    
    def create_account(self, username, password):
        check = self.validate_new_account(username, password)
        if check != "valid":
            return check

        accounts = self.load_accounts()

        accounts[username] = {
            "password": password,
            "balance": Constants.STARTING_BALANCE, # default balance for new accounts

            "stats": {
                "games_played": 0, # total amount of games played
                "wins": 0, # amount of games won
                "losses": 0, # amount of games lost
                "money_won": 0, # amount of money won
                "money_lost": 0
            }
        }

        self.save_accounts(accounts)
        return "Account created!"
    
    def login(self, username, password):
        # Allows user to login to their account
        username = username.strip()
        password = password.strip()
        if username == "":
            return False, "Please enter a username." # user didn't type in a username

        if password == "":
            return False, "Please enter a password." # user didn't type in a password

        accounts = self.load_accounts() # loads accounts to check if the details match

        if username not in accounts: # username isn't in the accounts list
            return False, "Incorrect Username."

        if accounts[username]["password"] != password: # password is incorrect
            return False, "Incorrect Password."

        return True, accounts[username] # user successfully logged in
    
    def validate_new_account(self, username, password):
        username = username.strip()
        password = password.strip()

        if username == "":
            return "Please enter a username."

        if password == "":
            return "Please enter a password."

        if len(username) < Constants.MIN_USERNAME_LENGTH:
            return f"Username must be at least {Constants.MIN_USERNAME_LENGTH} characters."
        
        if len(username) > Constants.MAX_USERNAME_LENGTH:
            return f"Username must be less than {Constants.MAX_USERNAME_LENGTH} characters."

        if len(password) < Constants.MIN_PASSWORD_LENGTH:
            return f"Password must be at least {Constants.MIN_PASSWORD_LENGTH} characters."
        
        if len(password) > Constants.MAX_PASSWORD_LENGTH:
            return f"Password must be less than {Constants.MAX_PASSWORD_LENGTH} characters."
        
        accounts = self.load_accounts()
        if username in accounts:
            return "Username already exists."

        return "valid"
    
    def update_account(self, username, account):
        # Updates account info when necessary
        accounts = self.load_accounts()
        accounts[username] = account
        self.save_accounts(accounts)


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
        """Deals a certain amount of cards and returns them as a list.
        Put an integer as the argument to deal that many cards
        In the game code, type: [hand var].extend([game var].deal_cards([num]))"""
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
    
    def natural_blackjack(self, hand):
        # Returns True if the hand is a natural blackjack
        return len(hand) == 2 and self.hand_value(hand) == 21

    def check_natural_blackjack(self):
        player = self.natural_blackjack(self.player_hand)
        dealer = self.natural_blackjack(self.dealer_hand)

        if player and dealer:
            return "Draw"

        elif player:
            return "Player wins!"

        elif dealer:
            return "Dealer wins!"

        return None

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
            return "Dealer wins!"

        elif dealer > 21:
            return "Player wins!"
        
        elif player > dealer:
            return "Player wins!"
        
        elif dealer > player:
            return "Dealer wins!"
        
        return "Draw"


class CasinoGUI:
    '''Class that handles the GUI, shows the windows that the user interacts with.'''
    def __init__(self, root):
        self.root = root
        self.root.title(Constants.CASINO_NAME)
        self.root.geometry(Constants.WINDOW_SIZE)
        self.accounts = Accounts()

        # Displays header
        self.create_header()

        # Account info
        self.current_username = ""
        self.current_user = None

        # Betting info
        self.current_bet = 0
        self.game_finished = False

        # Displays the page that the user is on
        self.content_frame = tk.Frame(self.root, bg=Constants.BG_COLOUR)
        self.content_frame.pack(fill="both", expand=True)

        # Function to load welcome screen for users to login or register
        self.show_welcome()

    def clear_content(self):
        # Resets the frame before showing a new page
        for widget in self.content_frame.winfo_children(): # I used tutorialspoint.com to find this tkinter function
            widget.destroy()

    def show_welcome(self):
        self.clear_content()

        self.welcome_frame = tk.Frame(self.content_frame, bg=Constants.BG_COLOUR)
        self.welcome_frame.pack(fill="both", expand=True)

        title = tk.Label(self.welcome_frame, text="Welcome to\nmy Casino!", bg=Constants.BG_COLOUR, fg=Constants.WHITE, font=Constants.TITLE_FONT)
        title.pack(pady=60)

        login_button = tk.Button(self.welcome_frame, text="LOGIN", bg=Constants.MAIN_COLOUR, font=Constants.MD_FONT, command=self.login_popup)
        login_button.pack(pady=15)

        register_button = tk.Button(self.welcome_frame, text="CREATE ACCOUNT", bg=Constants.MAIN_COLOUR, font=Constants.MD_FONT, command=self.register_popup)
        register_button.pack()

    def login_popup(self):
            window = tk.Toplevel(self.root)

            window.title("Login")
            window.geometry("300x220")
            window.resizable(False, False)

            # Username entry
            tk.Label(window, text="Username").pack(pady=(15,0))
            username_entry = tk.Entry(window)
            username_entry.pack()

            # Password entry
            tk.Label(window, text="Password").pack(pady=(10,0))
            password_entry = tk.Entry(window, show="*")
            password_entry.pack()

            def submit():
                success, result = self.accounts.login(username_entry.get(), password_entry.get())

                if success:
                    self.current_username = username_entry.get()
                    self.current_user = result

                    window.destroy()
                    self.show_homepage()
                    self.update_header()

                else:
                    messagebox.showerror("Login Failed", result)

            tk.Button(window, text="Login", command=submit).pack(pady=20)

    def register_popup(self):
        window = tk.Toplevel(self.root)
        window.title("Create Account")
        window.geometry("300x260")
        window.resizable(False, False)

        # Username entry
        tk.Label(window, text="Username").pack(pady=(15, 0))
        username_entry = tk.Entry(window)
        username_entry.pack()

        # Password entry
        tk.Label(window, text="Password").pack(pady=(10, 0))
        password_entry = tk.Entry(window, show="*")
        password_entry.pack()

        # Password confirmation (repeat password)
        tk.Label(window, text="Confirm Password").pack(pady=(10, 0))
        confirm_entry = tk.Entry(window, show="*")
        confirm_entry.pack()

        def submit():
            username = username_entry.get()
            password = password_entry.get()
            confirm = confirm_entry.get()

            if password != confirm:
                messagebox.showerror("Password Error", "Passwords do not match.")
                return

            result = self.accounts.create_account(username, password)

            if result == "Account created!":
                messagebox.showinfo("Success", "Account created successfully!")

                success, account = self.accounts.login(username, password)
                self.current_username = username
                self.current_user = account

                window.destroy()
                self.show_homepage()
                self.update_header()

            else:
                messagebox.showerror("Account Creation Failed", result) # Error message if the process failed

        tk.Button(
            window,
            text="Create Account",
            command=submit
        ).pack(pady=20)

    def create_header(self):
        self.header_frame = tk.Frame(self.root, bg=Constants.MAIN_COLOUR)
        self.header_frame.pack(fill="x", side="top")

        self.header_frame.columnconfigure([0, 3], weight=2)
        self.header_frame.columnconfigure([1, 2], weight=3) # middle columns are slightly wider to allow room for title
        self.header_frame.rowconfigure(0, weight=1)

        # Username display
        self.username_label = tk.Label(self.header_frame, text="", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.MD_FONT)
        self.username_label.grid(row=0, column=0, sticky="nsew", pady=8)

        # Casino title
        self.title_label = tk.Label(self.header_frame, text=Constants.CASINO_NAME, bg=Constants.MAIN_COLOUR, fg="black", font=Constants.TITLE_FONT)
        self.title_label.grid(row=0, column=1, columnspan=2, sticky="nsew", pady=8)

        # Balance
        self.balance_label = tk.Label(self.header_frame, text="", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.MD_FONT)
        self.balance_label.grid(row=0, column=3, sticky="nsew", pady=8)

    def update_header(self):
        self.username_label.config(text=self.current_username)
        self.balance_label.config(text=f"${self.current_user['balance']:.2f}")

    def show_homepage(self):
        self.clear_content()

        # ----- HOME PAGE    -----

        self.homepage = tk.Frame(self.content_frame, bg=Constants.BG_COLOUR)
        self.homepage.pack(fill="both", expand=True)

        self.homepage.rowconfigure(0, weight=1) # Header row
        self.homepage.rowconfigure([1, 2, 3, 4], weight=3)
        self.homepage.columnconfigure([0, 1, 2, 3], weight=1)

        # Button screen
        self.blackjack_button = tk.Button(self.homepage, text="BLACKJACK", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.LG_FONT, borderwidth=0, command=self.blackjack_bet_popup)
        self.blackjack_button.grid(row=1, column=0, columnspan=2, rowspan=2, padx=(32, 16), pady=(32, 16), sticky="nsew")

        self.slots_button = tk.Button(self.homepage, text="SLOTS", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.LG_FONT, borderwidth=0)
        self.slots_button.grid(row=1, column=2, columnspan=2, rowspan=2, padx=(16, 32), pady=(32, 16), sticky="nsew")

        self.highlow_button = tk.Button(self.homepage, text="HIGH/LOW", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.LG_FONT, borderwidth=0)
        self.highlow_button.grid(row=3, column=0, columnspan=2, rowspan=2, padx=(32, 16), pady=(16, 32), sticky="nsew")

        # Profile/Leaderboard container
        self.info_frame = tk.Frame(self.homepage, bg=Constants.BG_COLOUR)
        self.info_frame.grid(row= 3, column=2, columnspan=2, rowspan=2, padx=(16, 32), pady=(16, 32), sticky="nsew")

        self.info_frame.rowconfigure([0, 1], weight=1)
        self.info_frame.columnconfigure(0, weight=1)

        self.leaderboard_button = tk.Button(self.info_frame, text="LEADERBOARD", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.LG_FONT, borderwidth=0, command=self.show_leaderboard)
        self.leaderboard_button.grid(row=0, column=0, pady=(0, 16), sticky="nsew")

        self.profile_button = tk.Button(self.info_frame, text="PROFILE", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.LG_FONT, borderwidth=0)
        self.profile_button.grid(row=1, column=0, pady=(16, 0), sticky="nsew")

    def show_leaderboard(self):
        self.clear_content()
        lb_frame = tk.Frame(self.content_frame, bg=Constants.BG_COLOUR)
        lb_frame.pack(fill="both", expand=True)

        title = tk.Label(lb_frame, text="LEADERBOARD", bg=Constants.BG_COLOUR, fg=Constants.WHITE, font=Constants.TITLE_FONT)
        title.pack(pady=24)

        accounts = self.accounts.load_accounts()
        leaderboard = sorted(accounts.items(), key=lambda account: account[1]["balance"], reverse=True)

        header = tk.Frame(lb_frame, bg=Constants.MAIN_COLOUR)
        header.pack(fill="x", padx=80)

        header.columnconfigure([0, 1, 2], weight=1)

        tk.Label(header, text="Rank", bg=Constants.MAIN_COLOUR, fg="black",  font=Constants.SM_FONT_BOLD, width=8).grid(row=0, column=0, sticky="w", pady=10)
        tk.Label(header, text="Username", bg=Constants.MAIN_COLOUR, fg="black",  font=Constants.SM_FONT_BOLD, width=20).grid(row=0, column=1, sticky="we", pady=12)
        tk.Label(header, text="Balance", bg=Constants.MAIN_COLOUR, fg="black",  font=Constants.SM_FONT_BOLD, width=15).grid(row=0, column=2, sticky="e", pady=12)

        for rank, (username, account) in enumerate(leaderboard[:8], start=1):
            row=tk.Frame(lb_frame, bg="#2a2528")
            row.pack(fill="x", padx=80, pady=2)

            row.columnconfigure([0, 1, 2], weight=1)

            tk.Label(row, text=str(rank), bg="#2a2528", fg=Constants.WHITE, font=Constants.SM_FONT_BOLD, width=8).grid(row=0, column=0, sticky="w", pady=8)
            tk.Label(row, text=username, bg="#2a2528", fg=Constants.WHITE, font=Constants.SM_FONT, width=20).grid(row=0, column=1, sticky="w", pady=8)
            tk.Label(row, text=f"${account['balance']:.2f}", bg="#2a2528", fg=Constants.WHITE, font=Constants.SM_FONT, width=15).grid(row=0, column=2, sticky="e", pady=8)
        
        back_button = tk.Button(lb_frame, text="BACK", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.SM_FONT_BOLD, command=self.show_homepage)
        back_button.pack(pady=30)

    # ----- Betting Functions -----
        
    def save_player(self):
        # Saves the current player's information and updates the header
        self.accounts.update_account(self.current_username, self.current_user)
        self.update_header()

    def place_bet(self, bet):
        # Removes the bet from the player's balance
        self.current_bet = bet
        self.current_user["balance"] -= bet
        self.save_player()
        
    def validate_bet(self, bet):
        # Makes sure the bet is valid
        try:
            bet = int(bet)

        except ValueError:
            return False, "Please enter a whole number."

        if bet <= 0:
            return False, "Bet must be greater than $0."

        if bet > self.current_user["balance"]:
            return False, "You do not have enough money."

        return True, bet
    
    def update_stats(self, result):
        # Updates the player's statistics
        stats = self.current_user["stats"]
        stats["games_played"] += 1

        if result == "win":
            stats["wins"] += 1
            stats["money_won"] += self.current_bet

        elif result == "loss":
            stats["losses"] += 1
            stats["money_lost"] += self.current_bet
    
    def blackjack_bet_popup(self):
        """Shows a popup allowing the player to place a bet before Blackjack starts."""

        window = tk.Toplevel(self.root)
        window.title("Place Your Bet")
        window.geometry("300x220")
        window.resizable(False, False)

        # Make sure the popup stays in front
        window.transient(self.root)
        window.grab_set()

        # Title
        tk.Label(window, text="BLACKJACK", font=Constants.LG_FONT).pack(pady=(20, 5))

        # Current balance
        tk.Label(window, text=f"Balance: ${self.current_user['balance']:.2f}", font=Constants.SM_FONT).pack(pady=5)

        # Bet label
        tk.Label(window, text="Enter your bet:").pack(pady=(10, 2))

        bet_entry = tk.Entry(window)
        bet_entry.pack()

        def confirm_bet():
            # Get the bet entered by the player
            bet = bet_entry.get()

            # Validate the bet
            valid, result = self.validate_bet(bet)

            if not valid:
                messagebox.showerror("Invalid Bet", result)
                return

            # Place the bet
            self.place_bet(result)
            window.destroy()

            # Start the game after the bet has been placed
            self.show_blackjack()

        tk.Button(window, text="PLACE BET", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.SM_FONT_BOLD, command=confirm_bet).pack(pady=20)


    # ----- Blackjack Game -----
            
    def show_blackjack(self):
        # Starts a new game
        self.clear_content()
        self.game = BlackJack()
        self.game.deal_start()

        # Green table (background for game)
        self.blackjack_screen = tk.Frame(self.content_frame, bg=Constants.TABLE_COLOUR, highlightbackground=Constants.MAIN_COLOUR, highlightthickness=6)
        self.blackjack_screen.pack(fill="both", expand=True, padx=64, pady=32)

        self.blackjack_screen.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7], weight=1)
        self.blackjack_screen.columnconfigure([0, 1, 2, 3, 4, 5, 6], weight=1)

        # Dealer cards
        self.dealer_frame = tk.Frame(self.blackjack_screen, bg=Constants.TABLE_COLOUR)
        self.dealer_frame.grid(row=1, column=2, columnspan=3)

        # Dealer label
        self.dealer_total = tk.Label(self.blackjack_screen, text="Dealer", bg=Constants.TABLE_COLOUR, font=Constants.MD_FONT)
        self.dealer_total.grid(row=2, column=3)

        # Deck
        self.deck_card = self.create_card(self.blackjack_screen, hidden=True)
        self.deck_card.grid(row=2, column=0)

        # Player label
        self.player_total = tk.Label(self.blackjack_screen, text="You", bg=Constants.TABLE_COLOUR, font=Constants.MD_FONT)
        self.player_total.grid(row=4, column=3)

        # Player cards
        self.player_frame = tk.Frame(self.blackjack_screen, bg=Constants.TABLE_COLOUR)
        self.player_frame.grid(row=5, column=1, columnspan=5)

        # Draw starting cards
        self.update_blackjack_gui()

        # Buttons
        self.create_blackjack_buttons()

        # Winner label
        self.result_label = tk.Label(self.content_frame, text="", bg=Constants.BG_COLOUR, fg=Constants.WHITE, font=Constants.MD_FONT)
        self.result_label.pack(pady=10)

        winner = self.game.check_natural_blackjack()

        if winner is not None:
            self.finish_game()

    def create_card(self, parent, card=None, hidden=False):
        # This is how each card is displayer
        if hidden:
            # If a card is supposed to be hidden
            background = Constants.CARD_BACK_COLOUR
            foreground = Constants.WHITE
            text = "?"

        else:
            # All visible cards
            value, suit = card
            background = Constants.CARD_FRONT_COLOUR
            if suit == "♠" or suit == "♣":
                foreground = "black"
            else:
                foreground = "red"
            text = f"{value}\n{suit}"

        card_label = tk.Label(parent, text=text, bg=background, fg=foreground, width=4, height=3, relief="solid", borderwidth=2, font=Constants.MD_FONT)

        return card_label
    
    def draw_player_hand(self):
        for widget in self.player_frame.winfo_children():
            widget.destroy()

        # Displays the players cards
        for index, card in enumerate(self.game.player_hand):
            card_widget = self.create_card(self.player_frame, card=card)
            card_widget.grid(row=0, column=index, padx=10)
    
    def draw_dealer_hand(self, reveal=False):
        for widget in self.dealer_frame.winfo_children():
            widget.destroy()

        for index, card in enumerate(self.game.dealer_hand):

            if index == 0 and not reveal: # Hides one of the dealers card (while leaving the other visible)
                card_widget = self.create_card(self.dealer_frame, hidden=True)

            else: # shows all cards
                card_widget = self.create_card(self.dealer_frame, card=card)

            card_widget.grid(row=0, column=index, padx=10)

    def update_blackjack_gui(self, reveal=False):
        # Updates screen when new card is drawn
        self.draw_player_hand()
        self.draw_dealer_hand(reveal)

        # Players score
        self.player_total.config(text=f"You ({self.game.hand_value(self.game.player_hand)})")

        # Dealers score (only revealed at end)
        if reveal:
            self.dealer_total.config(text=f"Dealer ({self.game.hand_value(self.game.dealer_hand)})")

        else:
            self.dealer_total.config(text="Dealer")
    
    def create_blackjack_buttons(self):
        # Buttons for user to press
        self.button_frame = tk.Frame(self.content_frame, bg=Constants.BG_COLOUR)
        self.button_frame.pack(fill="x", pady=15)

        # Hit button
        self.hit_button = tk.Button(self.button_frame, text="HIT", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.MD_FONT, command=self.hit)
        self.hit_button.pack(side="left", expand=True, padx=20)

        # Stand button
        self.stand_button = tk.Button(self.button_frame, text="STAND", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.MD_FONT, command=self.stand)
        self.stand_button.pack(side="left", expand=True, padx=20)

        self.quit_button = tk.Button(self.button_frame, text="QUIT", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.MD_FONT, command=self.quit_blackjack)
        self.quit_button.pack(side="left", expand=True, padx=20)
    
    def hit(self):
        self.game.hit()
        self.update_blackjack_gui()

        # If user busts
        if self.game.game_over:
            self.finish_game()
        
        # If user gets exactly 21
        if self.game.hand_value(self.game.player_hand) == 21:
            self.stand()
    
    def stand(self):
        # Plays dealers turn
        self.game.dealer_turn()
        self.finish_game()
    
    def finish_game(self):
        self.update_blackjack_gui(True)
        # Finds and displays winner
        winner = self.game.find_winner()
        self.result_label.config(text=winner)

        # Disables hit and stand buttons so that user can't click them
        self.hit_button.config(state="disabled")
        self.stand_button.config(state="disabled")

        # Update balance and statistics
        if winner == "Player wins!":
            # Return the original bet and add winnings
            self.current_user["balance"] += self.current_bet * 2 
            self.update_stats("win") 
        
        elif winner == "Dealer wins!": self.update_stats("loss")

        elif winner == "Draw":
            # Return the original bet because nobody won 
            self.current_user["balance"] += self.current_bet

        # Save the updated account 
        self.save_player()

    
    def quit_blackjack(self):
        self.clear_content()
        self.show_homepage()


# Main program Function
def main():
    root = tk.Tk()
    app = CasinoGUI(root)
    root.mainloop()

# Runs Program
main()