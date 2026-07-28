import tkinter as tk

class CasinoGUI:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Red Clover Casino")
        self.root.geometry("800x600")

        # Home page

        self.homepage = tk.Frame(self.root, bg="#1f1b1d")
        self.homepage.pack(fill="both", expand=True)

        self.homepage.rowconfigure(0, weight=1) # Header row
        self.homepage.rowconfigure([1, 2, 3, 4], weight=3)
        self.homepage.columnconfigure([0, 1, 2, 3], weight=1)

        # Header frame

        self.header_frame = tk.Frame(self.homepage, bg="#d4142a")
        self.header_frame.grid(row=0, column=0, columnspan=4, sticky="nsew")

        self.header_frame.columnconfigure([0, 3], weight=2)
        self.header_frame.columnconfigure([1, 2], weight=3) # middle columns are slightly wider to allow room for title
        self.header_frame.rowconfigure(0, weight=1)

        self.username_label = tk.Label(self.header_frame, text="[username]", bg="#d4142a", fg="black", font="Arial 16 bold")
        self.username_label.grid(row=0, column=0, sticky="nsew")

        self.title_label = tk.Label(self.header_frame, text="Red Clover Casino", bg="#d4142a", fg="black", font="Arial 28 bold")
        self.title_label.grid(row=0, column=1, columnspan=2, sticky="nsew")

        self.balance_label = tk.Label(self.header_frame, text="$67.67", bg="#d4142a", fg="black", font="Arial 16 bold")
        self.balance_label.grid(row=0, column=3, sticky="nsew")

        # Button screen

        self.blackjack_button = tk.Button(self.homepage, text="BLACKJACK", bg="#d4142a", fg="black", font="Arial 22 bold")
        self.blackjack_button.grid(row=1, column=0, columnspan=2, rowspan=2, ipadx=(32, 16), ipady=(32, 16), sticky="nsew")

        self.slots_button = tk.Button(self.homepage, text="SLOTS", bg="#d4142a", fg="black", font="Arial 22 bold")
        self.slots_button.grid(row=1, column=2, columnspan=2, rowspan=2, ipadx=(16, 32), ipady=(32, 16), sticky="nsew")

        self.highlow_button = tk.Button(self.homepage, text="HIGH/LOW", bg="#d4142a", fg="black", font="Arial 22 bold")
        self.highlow_button.grid(row=3, column=0, columnspan=2, rowspan=2, ipadx=(32, 16), ipady=(16, 32), sticky="nsew")

        self.leaderboard_button = tk.Button(self.homepage, text="LEADERBOARD", bg="#d4142a", fg="black", font="Arial 22 bold")
        self.leaderboard_button.grid(row=3, column=2, columnspan=2, ipadx=(16, 32), ipady=16, sticky="nsew")

        self.profile_button = tk.Button(self.homepage, text="PROFILE", bg="#d4142a", fg="black", font="Arial 22 bold")
        self.profile_button.grid(row=4, column=2, columnspan=2, ipadx=(16, 32), ipady=(16, 32), sticky="nsew")


# Main program Function
def main():
    root = tk.Tk()
    app = CasinoGUI(root)
    root.mainloop()


# Runs Program
main()