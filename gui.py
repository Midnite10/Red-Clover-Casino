import tkinter as tk

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
        self.blackjack_button = tk.Button(self.homepage, text="BLACKJACK", bg="#d4142a", fg="black", font="Arial 22 bold", borderwidth=0)
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
        self.blackjack_screen = tk.Frame(self.content_frame, bg="#288a42")
        self.blackjack_screen.pack(fill="both", anchor="center", padx=64, pady=64)

        self.blackjack_screen.rowconfigure([0, 1])



# Main program Function
def main():
    root = tk.Tk()
    app = CasinoGUI(root)
    root.mainloop()


# Runs Program
main()