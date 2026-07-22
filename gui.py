import tkinter as tk

class CasinoGUI:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Red Clover Casino")
        self.root.geometry("800x600")


# Main program Function
def main():
    root = tk.Tk()
    app = CasinoGUI(root)
    root.mainloop()


# Runs Program
main()