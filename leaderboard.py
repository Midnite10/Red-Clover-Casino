import tkinter as tk

def show_leaderboard(self):
    self.clear_content()
    lb_frame = tk.Frame(self.content_frame, bg="#1f1b1d")
    lb_frame.pack(fill="both", expand=True)

    title = tk.Label(lb_frame, text="LEADERBOARD", bg="#1f1b1d", fg="white", font="Arial 28 bold")
    title.pack(pady=24)

    accounts = self.accounts.load_accounts()
    leaderboard = sorted(accounts.items(), key=lambda account: account[1]["balance"], reverse=True)

    header = tk.Frame(lb_frame, bg="#d4142a")
    header.pack(fill="x", padx=80)

    header.columnconfigure([0, 1, 2], weight=1)

    tk.Label(header, text="Rank", bg="#d4142a", fg="black",  font="Arial 14 bold", width=8).grid(row=0, column=0, sticky="w", pady=10)
    tk.Label(header, text="Username", bg="#d4142a", fg="black",  font="Arial 14 bold", width=20).grid(row=0, column=1, sticky="we", pady=12)
    tk.Label(header, text="Balance", bg="#d4142a", fg="black",  font="Arial 14 bold", width=15).grid(row=0, column=2, sticky="e", pady=12)

    for rank, (username, account) in enumerate(leaderboard[:10], start=1):
        row=tk.Frame(lb_frame, bg="#2a2528")
        row.pack(fill="x", padx=80, pady=2)

        row.columnconfigure([0, 1, 2], weight=1)

        tk.Label(row, text=str(rank), bg="#2a2528", fg="white", font="Arial 14 bold", width=8).grid(row=0, column=0, sticky="w", pady=8)
        tk.Label(row, text=username, bg="#2a2528", fg="white", font="Arial 14", width=20).grid(row=0, column=1, sticky="w", pady=8)
        tk.Label(row, text=f"${account['balance']:.2f}", bg="#2a2528", fg="white", font="Arial 14", width=15).grid(row=0, column=2, sticky="e", pady=8)

    back_button = tk.Button(lb_frame, text="BACK", bg="#d4142a", fg="black", font="Arial 14 bold", command=self.show_homepage)
    back_button.pack(pady=30)