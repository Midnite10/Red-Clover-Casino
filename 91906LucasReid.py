""" ----- Red Clover Casino -----
This is a casino project made for my NCEA AS91906.
Play blackjack, slot machine, and earn money to
get to the top of the leaderboard.

Project Contents:
- Constants
- Accounts
- PlayingCards
- Blackjack
- SlotMachine
- CasinoGUI

Made by: Lucas Reid
"""
import tkinter as tk
from tkinter import messagebox, ttk
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
    GREY = "#2a2528" # grey colour to differ from bg colour

    # ----- Fonts -----
    TITLE_FONT = "Arial 28 bold"
    LG_FONT = "Arial 22 bold"
    MD_FONT = "Arial 18 bold"
    SM_FONT = "Arial 14"
    SM_FONT_BOLD = "Arial 14 bold"

    # ----- Buttons -----
    LG_BUTTON_WIDTH = 24
    MD_BUTTON_WIDTH = 16
    SM_BUTTON_WIDTH = 8
    BTN_HEIGHT = 1

    # ----- Accounts -----
    STARTING_BALANCE = 1000
    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 16
    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 32

    # ----- Betting -----
    MIN_BET = 1 # minimum amount of dollars user can bet

    # ----- Playing Cards -----
    BLACK_SUIT = "black" # clubs or spades
    RED_SUIT = "red" # hearts or diamonds

    # ----- Blackjack -----
    PAYOUT_MULTIPLIER = 2
    STARTING_CARDS = 2
    ADDITIONAL_CARDS = 1
    BLACKJACK_LIMIT = 21 # Where the blackjack line is set (21 is default)
    DEALER_LIMIT = 17 # Where the dealer stops hitting
    DEALER_DRAW_DELAY = 1000 # milliseconds

    # ----- Slot Machine -----
    SLOT_REEL_COUNT = 3
    SLOT_SYMBOLS = {
        "🍒": {"weight": 40, "payout": 2},
        "🍋": {"weight": 30, "payout": 3},
        "🍇": {"weight": 15, "payout": 10},
        "⭐": {"weight": 10, "payout": 25},
        "🍀": {"weight": 5, "payout": 100}
    }
    SLOT_SPIN_TIME = 3
    SLOT_SPIN_DELAY = 100

    # ----- Game results -----
    GAME_RESULT_DELAY = 1000 # time in milliseconds
    WINNER = "#00c853" # winning green colour
    LOSER = "#ff1744" # losing red colour
    DRAW = "#ffd600" # draw yellow colour
    SLOT_WIN_COLOUR = "#FFD700" # jackpot is hit


class Accounts:
    def __init__(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(folder, "accounts.json")

    def load_accounts(self):
        try:
            with open(self.filename, "r") as file:
                return json.load(file)

        except (FileNotFoundError, json.JSONDecodeError): # if file isn't found
            return {}
    
    def save_accounts(self, accounts):
        with open(self.filename, "w") as file:
            json.dump(accounts, file, indent=4)
    
    def create_account(self, username, password):
        username = username.strip()
        password = password.strip()

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
                "money_lost": 0 # amount of money lost
            }
        }

        self.save_accounts(accounts)
        return "Account created!"
    
    def login(self, username, password):
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
            return f"Username can't be more than {Constants.MAX_USERNAME_LENGTH} characters."

        if len(password) < Constants.MIN_PASSWORD_LENGTH:
            return f"Password must be at least {Constants.MIN_PASSWORD_LENGTH} characters."
        
        if len(password) > Constants.MAX_PASSWORD_LENGTH:
            return f"Password can't be more than {Constants.MAX_PASSWORD_LENGTH} characters."
        
        accounts = self.load_accounts()
        if username in accounts:
            return "Username already exists."

        return "valid"
    
    def update_account(self, username, account):
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
        self.clear_deck()
        for i in range(self.deck_count):
            for suit in self.suits:
                for value in self.values:
                    self.deck.append((value, suit))

    def shuffle_deck(self):
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
        
        while total > Constants.BLACKJACK_LIMIT and aces:
            total -= 10
            aces -= 1
        
        return total
    
    def natural_blackjack(self, hand):
        # Returns True if the hand is a natural blackjack
        return len(hand) == Constants.STARTING_CARDS and self.hand_value(hand) == Constants.BLACKJACK_LIMIT

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
        self.player_hand.extend(self.deck.deal_cards(Constants.STARTING_CARDS))
        self.dealer_hand.extend(self.deck.deal_cards(Constants.STARTING_CARDS))
    
    def hit(self):
        self.player_hand.extend(self.deck.deal_cards(Constants.ADDITIONAL_CARDS))

        if self.hand_value(self.player_hand) > Constants.BLACKJACK_LIMIT:
            self.game_over = True

    def find_winner(self):
        player = self.hand_value(self.player_hand)
        dealer = self.hand_value(self.dealer_hand)

        if player > Constants.BLACKJACK_LIMIT:
            return "Dealer wins!"

        elif dealer > Constants.BLACKJACK_LIMIT:
            return "Player wins!"
        
        elif player > dealer:
            return "Player wins!"
        
        elif dealer > player:
            return "Dealer wins!"
        
        return "Draw"


class SlotMachine:
    """Slot machine game logic. Creates and spins the reels."""
    def __init__(self):
        self.reels = []
        self.result = None
        self.payout = 0

    def get_random_symbol(self):
        # Gets the symbols and their weights
        symbols = list(Constants.SLOT_SYMBOLS.keys())
        weights = [symbol["weight"] for symbol in Constants.SLOT_SYMBOLS.values()]

        return rand.choices(symbols, weights=weights, k=1)[0]

    def spin(self):
        # Creates a random result for each reel
        self.reels = []
        for i in range(Constants.SLOT_REEL_COUNT):
            self.reels.append(self.get_random_symbol())

        self.result = self.check_result()
        return self.reels

    def check_result(self):
        # Checks if all three symbols match
        if self.reels[0] == self.reels[1] and self.reels[1] == self.reels[2]:
            self.payout = Constants.SLOT_SYMBOLS[self.reels[0]]["payout"]
            return "jackpot"

        self.payout = 0
        return "loss"
    
    def get_winnings(self, bet):
        # Calculates how much money the player receives
        return bet * self.payout
    

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
        self.blackjack_finished = False

        # Displays the page that the user is on
        self.content_frame = tk.Frame(self.root, bg=Constants.BG_COLOUR)
        self.content_frame.pack(fill="both", expand=True)

        # Function to load welcome screen for users to login or register
        self.show_welcome()

    def logout(self):
        """Confirms logout before returning to the welcome screen."""
        confirm = messagebox.askyesno("Log Out", "Are you sure you want to log out?")

        if not confirm:
            return

        self.current_username = ""
        self.current_user = None
        self.current_bet = 0
        self.blackjack_finished = False

        self.show_welcome()
        self.update_header()

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

        login_button = tk.Button(self.welcome_frame, text="LOGIN", bg=Constants.MAIN_COLOUR, font=Constants.MD_FONT, width=Constants.MD_BUTTON_WIDTH, height=Constants.BTN_HEIGHT, command=self.login_popup)
        login_button.pack(pady=15)

        register_button = tk.Button(self.welcome_frame, text="CREATE ACCOUNT", bg=Constants.MAIN_COLOUR, font=Constants.MD_FONT, width=Constants.MD_BUTTON_WIDTH, height=Constants.BTN_HEIGHT, command=self.register_popup)
        register_button.pack()

    def login_popup(self):
            window = tk.Toplevel(self.root)

            window.title("Login")
            window.geometry("300x220")
            window.resizable(False, False)
            window.config(bg=Constants.BG_COLOUR)

            # Username entry
            tk.Label(window, text="Username", bg=Constants.BG_COLOUR, fg=Constants.WHITE).pack(pady=(15,0))
            username_entry = tk.Entry(window)
            username_entry.pack()

            # Password entry
            tk.Label(window, text="Password", bg=Constants.BG_COLOUR, fg=Constants.WHITE).pack(pady=(10,0))
            password_entry = tk.Entry(window, show="*") # makes password appear as asterisks rather than the actual password
            password_entry.pack()

            def submit():
                success, result = self.accounts.login(username_entry.get(), password_entry.get())

                if success:
                    self.current_username = username_entry.get().strip()
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
        window.config(bg=Constants.BG_COLOUR)

        # Username entry
        tk.Label(window, text="Username", bg=Constants.BG_COLOUR, fg=Constants.WHITE).pack(pady=(15, 0))
        username_entry = tk.Entry(window)
        username_entry.pack()

        # Password entry
        tk.Label(window, text="Password", bg=Constants.BG_COLOUR, fg=Constants.WHITE).pack(pady=(10, 0))
        password_entry = tk.Entry(window, show="*")
        password_entry.pack()

        # Password confirmation (repeat password)
        tk.Label(window, text="Confirm Password", bg=Constants.BG_COLOUR, fg=Constants.WHITE).pack(pady=(10, 0))
        confirm_entry = tk.Entry(window, show="*")
        confirm_entry.pack()

        def submit():
            username = username_entry.get().strip()
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

        tk.Button(window, text="Create Account", command=submit).pack(pady=20)

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

        self.blackjack_button = tk.Button(self.homepage, text="BLACKJACK", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.LG_FONT, borderwidth=0, command=lambda: self.show_bet_screen(self.show_blackjack))
        self.blackjack_button.grid(row=1, column=0, columnspan=2, rowspan=2, padx=(32, 16), pady=(32, 16), sticky="nsew")

        self.slots_button = tk.Button(self.homepage, text="SLOTS", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.LG_FONT, borderwidth=0, command=lambda: self.show_bet_screen(self.show_slots))
        self.slots_button.grid(row=1, column=2, columnspan=2, rowspan=2, padx=(16, 32), pady=(32, 16), sticky="nsew")

        self.highlow_button = tk.Button(self.homepage, text="COMING SOON...", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.LG_FONT, borderwidth=0)
        self.highlow_button.grid(row=3, column=0, columnspan=2, rowspan=2, padx=(32, 16), pady=(16, 32), sticky="nsew")

        self.info_frame = tk.Frame(self.homepage, bg=Constants.BG_COLOUR)
        self.info_frame.grid(row= 3, column=2, columnspan=2, rowspan=2, padx=(16, 32), pady=(16, 32), sticky="nsew")

        self.info_frame.rowconfigure([0, 1], weight=1)
        self.info_frame.columnconfigure(0, weight=1)

        self.leaderboard_button = tk.Button(self.info_frame, text="LEADERBOARD", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.LG_FONT, borderwidth=0, command=self.show_leaderboard)
        self.leaderboard_button.grid(row=0, column=0, pady=(0, 16), sticky="nsew")

        self.profile_button = tk.Button(self.info_frame, text="PROFILE", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.LG_FONT, borderwidth=0, command=self.show_profile)
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

        tk.Label(header, text="Rank", bg=Constants.MAIN_COLOUR, fg="black",  font=Constants.SM_FONT_BOLD, width=8).grid(row=0, column=0, sticky="w", pady=8)
        tk.Label(header, text="Username", bg=Constants.MAIN_COLOUR, fg="black",  font=Constants.SM_FONT_BOLD, width=20).grid(row=0, column=1, sticky="we", pady=8)
        tk.Label(header, text="Balance", bg=Constants.MAIN_COLOUR, fg="black",  font=Constants.SM_FONT_BOLD, width=15).grid(row=0, column=2, sticky="e", pady=8)

        for rank, (username, account) in enumerate(leaderboard[:8], start=1):
            row=tk.Frame(lb_frame, bg="#2a2528")
            row.pack(fill="x", padx=80, pady=2)

            row.columnconfigure([0, 1, 2], weight=1)

            tk.Label(row, text=str(rank), bg="#2a2528", fg=Constants.WHITE, font=Constants.SM_FONT_BOLD, width=8).grid(row=0, column=0, sticky="w", pady=4)
            tk.Label(row, text=username, bg="#2a2528", fg=Constants.WHITE, font=Constants.SM_FONT, width=20).grid(row=0, column=1, sticky="w", pady=4)
            tk.Label(row, text=f"${account['balance']:.2f}", bg="#2a2528", fg=Constants.WHITE, font=Constants.SM_FONT, width=15).grid(row=0, column=2, sticky="e", pady=4)
        
        back_button = tk.Button(lb_frame, text="BACK", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.SM_FONT_BOLD, width=Constants.SM_BUTTON_WIDTH, height=Constants.BTN_HEIGHT, command=self.show_homepage)
        back_button.pack(pady=24)

    def show_profile(self):
        self.clear_content()

        profile_frame = tk.Frame(self.content_frame, bg=Constants.BG_COLOUR)
        profile_frame.pack(fill="both", expand=True)

        title = tk.Label(profile_frame, text="PROFILE", bg=Constants.BG_COLOUR, fg=Constants.WHITE, font=Constants.TITLE_FONT)
        title.pack(pady=(16, 12))

        # ----- Account information -----

        account_frame = tk.Frame(profile_frame, bg=Constants.GREY)
        account_frame.pack(fill="x", padx=120, pady=8)

        account_frame.columnconfigure(0, weight=1)
        account_frame.columnconfigure(1, weight=2)

        tk.Label(account_frame, text="Username", bg=Constants.GREY, fg=Constants.WHITE, font=Constants.SM_FONT_BOLD).grid(row=0, column=0, sticky="w", padx=20, pady=6)
        tk.Label(account_frame, text=self.current_username, bg=Constants.GREY, fg=Constants.WHITE, font=Constants.SM_FONT).grid(row=0, column=1, sticky="e", padx=20, pady=6)

        tk.Label(account_frame, text="Balance", bg=Constants.GREY, fg=Constants.WHITE, font=Constants.SM_FONT_BOLD).grid(row=1, column=0, sticky="w", padx=20, pady=6)
        tk.Label(account_frame, text=f"${self.current_user['balance']:.2f}", bg=Constants.GREY, fg=Constants.WHITE, font=Constants.SM_FONT).grid(row=1, column=1, sticky="e", padx=20, pady=6)

        # ----- Statistics -----

        stats_title = tk.Label(profile_frame, text="STATISTICS", bg=Constants.BG_COLOUR, fg=Constants.WHITE, font=Constants.LG_FONT)
        stats_title.pack(pady=(16, 8))

        stats_frame = tk.Frame(profile_frame, bg=Constants.GREY)
        stats_frame.pack(fill="x", padx=120, pady=8)

        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=2)

        stats = self.current_user["stats"]

        tk.Label(stats_frame, text="Games Played", bg=Constants.GREY, fg=Constants.WHITE, font=Constants.SM_FONT_BOLD).grid(row=0, column=0, sticky="w", padx=20, pady=6)
        tk.Label(stats_frame, text=str(stats["games_played"]),  bg=Constants.GREY, fg=Constants.WHITE, font=Constants.SM_FONT).grid(row=0, column=1, sticky="e", padx=20, pady=6)

        tk.Label(stats_frame, text="Wins", bg=Constants.GREY, fg=Constants.WHITE, font=Constants.SM_FONT_BOLD).grid(row=1, column=0, sticky="w", padx=20, pady=6)
        tk.Label(stats_frame, text=str(stats["wins"]), bg=Constants.GREY, fg=Constants.WHITE, font=Constants.SM_FONT).grid(row=1, column=1, sticky="e", padx=20, pady=6)

        tk.Label(stats_frame, text="Losses", bg="#2a2528", fg=Constants.WHITE, font=Constants.SM_FONT_BOLD).grid(row=2, column=0, sticky="w", padx=20, pady=6)
        tk.Label(stats_frame, text=str(stats["losses"]), bg="#2a2528", fg=Constants.WHITE,  font=Constants.SM_FONT ).grid(row=2, column=1, sticky="e", padx=20, pady=6)

        tk.Label(stats_frame, text="Money Won", bg="#2a2528", fg=Constants.WHITE, font=Constants.SM_FONT_BOLD ).grid(row=3, column=0, sticky="w", padx=20, pady=6)
        tk.Label(stats_frame, text=f"${stats['money_won']:.2f}", bg="#2a2528", fg=Constants.WHITE, font=Constants.SM_FONT).grid(row=3, column=1, sticky="e", padx=20, pady=6)

        tk.Label(stats_frame, text="Money Lost", bg="#2a2528", fg=Constants.WHITE, font=Constants.SM_FONT_BOLD).grid(row=4, column=0, sticky="w", padx=20, pady=6)
        tk.Label(stats_frame, text=f"${stats['money_lost']:.2f}", bg="#2a2528", fg=Constants.WHITE, font=Constants.SM_FONT).grid(row=4, column=1, sticky="e", padx=20, pady=6)

        # ----- Profile buttons -----
        button_frame = tk.Frame(profile_frame, bg=Constants.BG_COLOUR)
        button_frame.pack(pady=16)

        back_button = tk.Button(button_frame, text="BACK", bg=Constants.MAIN_COLOUR, fg=Constants.WHITE, font=Constants.SM_FONT_BOLD, width=Constants.SM_BUTTON_WIDTH, height=Constants.BTN_HEIGHT, command=self.show_homepage)
        back_button.pack(side="left", padx=8)

        logout_button = tk.Button(button_frame, text="LOG OUT", bg=Constants.MAIN_COLOUR, fg=Constants.WHITE, font=Constants.SM_FONT_BOLD, width=Constants.SM_BUTTON_WIDTH, height=Constants.BTN_HEIGHT, command=self.logout)
        logout_button.pack(side="left", padx=8)


    # ----- Betting Functions -----
        
    def save_player(self):
        self.accounts.update_account(self.current_username, self.current_user)
        self.update_header()

    def place_bet(self, bet):
        # Removes the bet from the player's balance
        self.current_bet = bet
        self.current_user["balance"] -= bet
        self.save_player()
        
    def validate_bet(self, bet):
        try:
            bet = int(bet)

        except ValueError:
            return False, "Please enter a whole number."

        if bet < Constants.MIN_BET:
            return False, f"Bet must be at least ${Constants.MIN_BET}."

        if bet > self.current_user["balance"]:
            return False, "You do not have enough money."

        return True, bet
    
    def update_stats(self, result):
        stats = self.current_user["stats"]
        stats["games_played"] += 1

        if result == "win":
            stats["wins"] += 1
            stats["money_won"] += self.current_bet

        elif result == "loss":
            stats["losses"] += 1
            stats["money_lost"] += self.current_bet
    
    def show_bet_screen(self, game_function):
        self.clear_content()

        bet_frame = tk.Frame(self.content_frame, bg=Constants.BG_COLOUR)
        bet_frame.pack(fill="both", expand=True)

        bet_frame.columnconfigure([0, 1, 2], weight=1)
        bet_frame.rowconfigure([0, 5], weight=2)
        bet_frame.rowconfigure([1, 2, 3, 4], weight=1)

        # ----- Title -----

        title = tk.Label(bet_frame, text="PLACE YOUR BET", bg=Constants.BG_COLOUR, fg=Constants.WHITE, font=Constants.TITLE_FONT)
        title.grid(row=0, column=0, columnspan=3, sticky="s", pady=(20, 10))

        balance_label = tk.Label(bet_frame, text=f"Balance: ${self.current_user['balance']:.2f}", bg=Constants.BG_COLOUR, fg=Constants.WHITE, font=Constants.MD_FONT)
        balance_label.grid(row=1, column=1, sticky="n", pady=10)

        bet_label = tk.Label(bet_frame, text="Select your bet:", bg=Constants.BG_COLOUR, fg=Constants.WHITE, font=Constants.SM_FONT_BOLD)
        bet_label.grid(row=2, column=1, sticky="s", pady=5)

        bet_options = []

        standard_bets = [1, 5, 10, 25, 50, 100, 250, 500, 1000, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000]

        for bet in standard_bets:
            if self.current_user["balance"] >= bet:
                bet_options.append(f"${bet}")

        if self.current_user["balance"] >= Constants.MIN_BET:
            bet_options.append("ALL IN")

        selected_bet = tk.StringVar()

        bet_dropdown = ttk.Combobox(bet_frame, textvariable=selected_bet, values=bet_options, state="normal", font=Constants.SM_FONT, width=15)
        bet_dropdown.grid(row=3, column=1, sticky="n", pady=10)

        if bet_options:
            bet_dropdown.set(bet_options[0])

        def confirm_bet():

            choice = selected_bet.get().strip()

            if choice == "":
                messagebox.showerror("Invalid Bet", "Please enter or select a bet.")
                return

            if choice.upper() == "ALL IN":
                bet = self.current_user["balance"]

            else:
                # Allow user to type "$###" or "###"
                choice = choice.replace("$", "").strip()
                valid, result = self.validate_bet(choice)

                if not valid:
                    messagebox.showerror("Invalid Bet", result)
                    return

                bet = result

            self.place_bet(bet)
            game_function()

        place_button = tk.Button(bet_frame, text="PLACE BET", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.MD_FONT, borderwidth=0, width=Constants.MD_BUTTON_WIDTH, height=Constants.BTN_HEIGHT, command=confirm_bet)
        place_button.grid(row=4, column=1, sticky="nsew", padx=80, pady=15)

        back_button = tk.Button(bet_frame, text="BACK", bg=Constants.GREY, fg=Constants.WHITE, font=Constants.SM_FONT_BOLD, borderwidth=0, width=Constants.MD_BUTTON_WIDTH, height=Constants.BTN_HEIGHT, command=self.show_homepage)
        back_button.grid(row=5, column=1, sticky="n", pady=20)

    def show_game_result(self, game_name, result, amount, game_function):
        self.clear_content()

        result_frame = tk.Frame(self.content_frame, bg=Constants.BG_COLOUR)
        result_frame.pack(fill="both", expand=True)

        result_frame.columnconfigure([0, 2], weight=1)
        result_frame.columnconfigure(1, weight=2)
            
        result_frame.rowconfigure([0, 5], weight=2)
        result_frame.rowconfigure([1, 2, 3, 4], weight=1)

        game_label = tk.Label(result_frame, text=game_name, bg=Constants.BG_COLOUR, fg=Constants.WHITE, font=Constants.TITLE_FONT)
        game_label.grid(row=0, column=0, columnspan=3, sticky="s", pady=(20, 5))

        if result == "win":
            result_text = "YOU WIN!"
            result_colour = Constants.WINNER

        elif result == "loss":
            result_text = "YOU LOSE!"
            result_colour = Constants.LOSER

        else:
            result_text = "DRAW"
            result_colour = Constants.DRAW

        result_label = tk.Label(result_frame, text=result_text, bg=Constants.BG_COLOUR, fg=result_colour, font=Constants.LG_FONT)
        result_label.grid(row=1, column=1, pady=10)

        if result == "win":
            money_text = f"You won ${amount:.2f}"

        elif result == "loss":
            money_text = f"You lost ${amount:.2f}"

        else:
            money_text = "Your bet was returned"

        money_label = tk.Label(result_frame, text=money_text, bg=Constants.BG_COLOUR, fg=Constants.WHITE, font=Constants.MD_FONT)
        money_label.grid(row=2, column=1, pady=10)

        balance_label = tk.Label(result_frame, text=f"Balance: ${self.current_user['balance']:.2f}", bg=Constants.BG_COLOUR, fg=Constants.WHITE, font=Constants.MD_FONT)
        balance_label.grid(row=3, column=1, pady=10)

        play_again_button = tk.Button(result_frame, text="PLAY AGAIN", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.MD_FONT, borderwidth=0, width=Constants.MD_BUTTON_WIDTH, height=Constants.BTN_HEIGHT, command=lambda: self.show_bet_screen(game_function))
        play_again_button.grid(row=4, column=1, sticky="nsew", padx=80, pady=10)

        home_button = tk.Button(result_frame, text="HOME", bg=Constants.GREY, fg=Constants.WHITE, font=Constants.SM_FONT_BOLD, borderwidth=0, width=Constants.MD_BUTTON_WIDTH, height=Constants.BTN_HEIGHT, command=self.show_homepage)
        home_button.grid(row=5, column=1, sticky="n", pady=20)

    def show_blackjack(self):
        # Starts a new game
        self.clear_content()

        self.blackjack_finished = False
        self.game = BlackJack()
        self.game.deal_start()

        self.blackjack_screen = tk.Frame(self.content_frame, bg=Constants.TABLE_COLOUR, highlightbackground=Constants.MAIN_COLOUR, highlightthickness=6)
        self.blackjack_screen.pack(fill="both", expand=True, padx=64, pady=32)

        self.blackjack_screen.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7], weight=1)
        self.blackjack_screen.columnconfigure([0, 1, 2, 3, 4, 5, 6], weight=1)

        self.dealer_frame = tk.Frame(self.blackjack_screen, bg=Constants.TABLE_COLOUR)
        self.dealer_frame.grid(row=1, column=2, columnspan=3)

        self.dealer_total = tk.Label(self.blackjack_screen, text="Dealer", bg=Constants.TABLE_COLOUR, font=Constants.MD_FONT)
        self.dealer_total.grid(row=2, column=3)

        self.deck_card = self.create_card(self.blackjack_screen, hidden=True)
        self.deck_card.grid(row=2, column=0)

        self.player_total = tk.Label(self.blackjack_screen, text="You", bg=Constants.TABLE_COLOUR, font=Constants.MD_FONT)
        self.player_total.grid(row=4, column=3)

        self.player_frame = tk.Frame(self.blackjack_screen, bg=Constants.TABLE_COLOUR)
        self.player_frame.grid(row=5, column=1, columnspan=5)

        self.update_blackjack_gui()

        self.create_blackjack_buttons()

        self.result_label = tk.Label(self.content_frame, text="", bg=Constants.BG_COLOUR, fg=Constants.WHITE, font=Constants.MD_FONT)
        self.result_label.pack(pady=10)

        winner = self.game.check_natural_blackjack()

        if winner is not None:
            self.finish_blackjack()

    def create_card(self, parent, card=None, hidden=False):
        if hidden:
            background = Constants.CARD_BACK_COLOUR
            foreground = Constants.WHITE
            text = "?"

        else:
            value, suit = card
            background = Constants.CARD_FRONT_COLOUR
            if suit == "♠" or suit == "♣":
                foreground = Constants.BLACK_SUIT
            else:
                foreground = Constants.RED_SUIT
            text = f"{value}\n{suit}"

        card_label = tk.Label(parent, text=text, bg=background, fg=foreground, width=4, height=3, relief="solid", borderwidth=2, font=Constants.MD_FONT)

        return card_label
    
    def draw_player_hand(self):
        for widget in self.player_frame.winfo_children():
            widget.destroy()

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
        self.draw_player_hand()
        self.draw_dealer_hand(reveal)

        self.player_total.config(text=f"You ({self.game.hand_value(self.game.player_hand)})")

        if reveal:
            self.dealer_total.config(text=f"Dealer ({self.game.hand_value(self.game.dealer_hand)})")

        else:
            self.dealer_total.config(text="Dealer")
    
    def create_blackjack_buttons(self):
        self.button_frame = tk.Frame(self.content_frame, bg=Constants.BG_COLOUR)
        self.button_frame.pack(fill="x", pady=15)

        self.hit_button = tk.Button(self.button_frame, text="HIT", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.MD_FONT, width=Constants.SM_BUTTON_WIDTH, height=Constants.BTN_HEIGHT, command=self.hit)
        self.hit_button.pack(side="left", expand=True, padx=20)

        self.stand_button = tk.Button(self.button_frame, text="STAND", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.MD_FONT, width=Constants.SM_BUTTON_WIDTH, height=Constants.BTN_HEIGHT, command=self.stand)
        self.stand_button.pack(side="left", expand=True, padx=20)

        self.quit_button = tk.Button(self.button_frame, text="QUIT", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.MD_FONT, width=Constants.SM_BUTTON_WIDTH, height=Constants.BTN_HEIGHT, command=self.quit_blackjack)
        self.quit_button.pack(side="left", expand=True, padx=20)
    
    def hit(self):
        self.game.hit()
        self.update_blackjack_gui()

        if self.game.game_over:
            self.finish_blackjack()

        elif self.game.hand_value(self.game.player_hand) == Constants.BLACKJACK_LIMIT:
            self.stand()
    
    def stand(self):
        self.hit_button.config(state="disabled")
        self.stand_button.config(state="disabled")

        self.update_blackjack_gui(True)
        self.root.after(Constants.DEALER_DRAW_DELAY, self.dealer_draw)

    def dealer_draw(self):

        if self.game.hand_value(self.game.dealer_hand) >= Constants.DEALER_LIMIT:
            self.finish_blackjack()
            return

        self.game.dealer_hand.extend(self.game.deck.deal_cards(Constants.ADDITIONAL_CARDS))

        self.update_blackjack_gui(True)
        self.root.after(Constants.DEALER_DRAW_DELAY, self.dealer_draw)
    
    def finish_blackjack(self):
        if self.blackjack_finished:
            return
        
        self.blackjack_finished = True

        self.update_blackjack_gui(True)
        winner = self.game.find_winner()

        if winner == "Player wins!":
            self.current_user["balance"] += (self.current_bet * Constants.PAYOUT_MULTIPLIER)
            self.update_stats("win")
            result = "win"

        elif winner == "Dealer wins!":
            self.update_stats("loss")
            result = "loss"

        else:
            self.current_user["balance"] += self.current_bet
            self.update_stats("draw")
            result = "draw"

        amount = self.current_bet
        self.save_player()
        self.root.after(Constants.GAME_RESULT_DELAY, lambda: self.show_game_result("BLACKJACK", result, amount, self.show_blackjack))

    
    def quit_blackjack(self):
        confirm = messagebox.askyesno("Quit Blackjack", "Are you sure you want to quit the game?\nYour bet will NOT be returned.")
        if not confirm:
            return

        self.clear_content()
        self.show_homepage()

    # ----- Slot Machine Game -----

    def show_slots(self):
        self.clear_content()
        self.slot_game = SlotMachine()

        self.slots_screen = tk.Frame(self.content_frame, bg=Constants.GREY, highlightbackground=Constants.MAIN_COLOUR, highlightthickness=6)
        self.slots_screen.pack(fill="both", expand=True, padx=64, pady=32)

        self.slots_screen.rowconfigure([0, 1, 2, 3, 4, 5], weight=1)
        self.slots_screen.columnconfigure([0, 1, 2, 3, 4], weight=1)

        title = tk.Label(self.slots_screen, text="SLOT MACHINE", bg=Constants.GREY, fg=Constants.WHITE, font=Constants.TITLE_FONT)
        title.grid(row=0, column=0, columnspan=5, pady=10)

        self.reel_frame = tk.Frame(self.slots_screen, bg=Constants.GREY)
        self.reel_frame.grid(row=2, column=1, columnspan=3)

        self.reel_labels = []

        for i in range(Constants.SLOT_REEL_COUNT):
            label = tk.Label(self.reel_frame, text="?", bg=Constants.CARD_FRONT_COLOUR, fg="black", width=5, height=2, relief="solid", borderwidth=3, font=Constants.TITLE_FONT)
            label.grid(row=0, column=i, padx=10)
            self.reel_labels.append(label)

        self.slot_result_label = tk.Label(self.slots_screen, text="Press SPIN to play!", bg=Constants.GREY, fg=Constants.WHITE, font=Constants.MD_FONT)
        self.slot_result_label.grid(row=3, column=0, columnspan=5)

        self.spin_button = tk.Button(self.slots_screen, text="SPIN", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.MD_FONT, width=Constants.MD_BUTTON_WIDTH, height=Constants.BTN_HEIGHT, command=self.spin_slots)
        self.spin_button.grid(row=4, column=1, columnspan=3, pady=10)

        self.quit_slots_button = tk.Button(self.slots_screen, text="QUIT", bg=Constants.GREY, fg=Constants.WHITE, font=Constants.SM_FONT_BOLD, width=Constants.SM_BUTTON_WIDTH, height=Constants.BTN_HEIGHT, command=self.quit_slots)
        self.quit_slots_button.grid(row=5, column=1, columnspan=3, pady=10)
    
    def spin_slots(self):
        self.spin_button.config(state="disabled")
        self.slot_result_label.config(text="SPINNING...", fg=Constants.WHITE)
        self.animate_slots(0)

    def animate_slots(self, spin_count):
        if spin_count < Constants.SLOT_SPIN_TIME * 10:
            for label in self.reel_labels:
                label.config(text=self.slot_game.get_random_symbol())

            self.root.after(Constants.SLOT_SPIN_DELAY, lambda: self.animate_slots(spin_count + 1))

        else:
            self.finish_slots()
    
    def finish_slots(self):
        reels = self.slot_game.spin()

        for index, symbol in enumerate(reels):
            self.reel_labels[index].config(text=symbol)

        winnings = self.slot_game.get_winnings(self.current_bet)

        if self.slot_game.result == "jackpot":
            for label in self.reel_labels:
                label.config(bg=Constants.SLOT_WIN_COLOUR)

            self.current_user["balance"] += winnings
            self.update_stats("win")
            result_text = f"JACKPOT! You won ${winnings:.2f}!"
            result_colour = Constants.WINNER

        else:
            for label in self.reel_labels:
                label.config(bg=Constants.LOSER)

            self.update_stats("loss")
            result_text = f"You lost ${self.current_bet:.2f}"
            result_colour = Constants.LOSER

        self.save_player()
        self.update_header()

        self.root.after(Constants.GAME_RESULT_DELAY, lambda: self.show_slots_result(result_text, result_colour))

    def show_slots_result(self, result_text, result_colour):
        self.clear_content()

        result_frame = tk.Frame(self.content_frame, bg=Constants.BG_COLOUR)
        result_frame.pack(fill="both", expand=True)

        # Grid configuration
        result_frame.columnconfigure([0, 1, 2], weight=1)
        result_frame.rowconfigure([0, 1, 2, 3, 4, 5, 6], weight=1)

        title = tk.Label(result_frame, text="SLOT MACHINE", bg=Constants.BG_COLOUR, fg=Constants.WHITE, font=Constants.TITLE_FONT)
        title.grid(row=0, column=0, columnspan=3, sticky="s", pady=10)

        result_label = tk.Label(result_frame, text=result_text, bg=Constants.BG_COLOUR, fg=result_colour, font=Constants.LG_FONT)
        result_label.grid(row=1, column=0, columnspan=3, pady=10)

        balance_label = tk.Label(result_frame, text=f"Balance: ${self.current_user['balance']:.2f}", bg=Constants.BG_COLOUR, fg=Constants.WHITE, font=Constants.MD_FONT)
        balance_label.grid(row=2, column=0, columnspan=3, pady=5)

        bet_label = tk.Label(result_frame, text=f"Current bet: ${self.current_bet:.2f}", bg=Constants.BG_COLOUR, fg=Constants.WHITE, font=Constants.SM_FONT)
        bet_label.grid(row=3, column=0, columnspan=3, pady=5)

        spin_again_button = tk.Button(result_frame, text="SPIN AGAIN", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.MD_FONT, borderwidth=0, width=Constants.MD_BUTTON_WIDTH, height=Constants.BTN_HEIGHT, command=self.show_slots)
        spin_again_button.grid(row=4, column=0, columnspan=3, padx=80, pady=15, sticky="nsew")

        change_bet_button = tk.Button(result_frame, text="CHANGE BET", bg=Constants.GREY, fg=Constants.WHITE, font=Constants.SM_FONT_BOLD, borderwidth=0, width=Constants.MD_BUTTON_WIDTH, height=Constants.BTN_HEIGHT, command=self.show_bet_screen(self.show_slots))
        change_bet_button.grid(row=5, column=0, columnspan=3, pady=15)

        quit_button = tk.Button(result_frame, text="QUIT", bg=Constants.GREY, fg=Constants.WHITE, font=Constants.SM_FONT_BOLD, borderwidth=0, width=Constants.MD_BUTTON_WIDTH, height=Constants.BTN_HEIGHT, command=self.show_homepage)
        quit_button.grid(row=6, column=0, columnspan=3, pady=15)

    def quit_slots(self):
        confirm = messagebox.askyesno("Quit Slot Machine", "Are you sure you want to quit the game?\n\nYour bet will NOT be returned.")
        if not confirm:
            return

        self.clear_content()
        self.show_homepage()


# Main program Function
def main():
    root = tk.Tk()
    app = CasinoGUI(root)
    root.mainloop()

main()