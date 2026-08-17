def show_bet_screen(self, game_function):

        self.clear_content()

        # Main betting screen
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

        # ----- Create bet options based on balance -----

        bet_options = []

        standard_bets = [1, 5, 10, 25, 50, 100, 250, 500]

        for bet in standard_bets:
            if self.current_user["balance"] >= bet:
                bet_options.append(f"${bet}")

        # Add ALL IN if user can afford the minimum bet
        if self.current_user["balance"] >= Constants.MIN_BET:
            bet_options.append("ALL IN")

        # ----- Editable dropdown -----

        selected_bet = tk.StringVar()

        bet_dropdown = ttk.Combobox(bet_frame, textvariable=selected_bet, values=bet_options, state="normal", font=Constants.SM_FONT, width=15)
        bet_dropdown.grid(row=3, column=1, sticky="n", pady=10)

        # Set default value
        if bet_options:
            bet_dropdown.set(bet_options[0])

        # ----- Confirm bet -----

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
            self.show_blackjack()
            game_function()

        place_button = tk.Button(bet_frame, text="PLACE BET", bg=Constants.MAIN_COLOUR, fg="black", font=Constants.MD_FONT, borderwidth=0, command=confirm_bet)
        place_button.grid(row=4, column=1, sticky="nsew", padx=80, pady=15)

        back_button = tk.Button(bet_frame, text="BACK", bg=Constants.GREY, fg=Constants.WHITE, font=Constants.SM_FONT_BOLD, borderwidth=0, command=self.show_homepage)
        back_button.grid(row=5, column=1, sticky="n", pady=20)