import json


class Accounts:
    # Manages the accounts system for the casino
    def __init__(self):
        self.filename = "accounts.json" # json file containing all accounts

    def load_accounts(self):
        # loads accounts onto program
        try:
            with open(self.filename, "r") as file:
                return json.load(file)

        except FileNotFoundError: # if file isn't found
            return {}
    
    def save_accounts(self, accounts):
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
            "balance": 1000, # 1000 is default balance for new accounts

            "stats": {
                "games_played": 0, # total amount of games played
                "wins": 0, # amount of games won
                "losses": 0, # amount of games lost
                "money_won": 0 # amount of money won
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

        if len(username) < 3:
            return "Username must be at least 3 characters."
        
        if len(username) > 16:
            return "Username must be less than 16 characters."

        if len(password) < 4:
            return "Password must be at least 4 characters."
        
        if len(password) > 32:
            return "Password must be less than 32 characters."
        
        accounts = self.load_accounts()
        if username in accounts:
            return "Username already exists."

        return "valid"
    
    def update_account(self, username, account):
        # Updates account info when necessary
        accounts = self.load_accounts()
        accounts[username] = account
        self.save_accounts(accounts)