import tkinter as tk
from modules.database import get_connection

class MotivateMe:
    def __init__(self, root):
        self.root = root
        self.root.title("Motivate Me")
        self.frame = tk.Frame(root, bg="#f0f2f5")
        self.frame.pack(expand=True, fill="both", padx=20, pady=20)

        tk.Label(
            self.frame, text="Motivational Quotes", font=("Segoe UI", 16, "bold"),
            bg="#f0f2f5", fg="#333"
        ).pack(pady=(10, 20))

        # Quote box like a card
        self.quote_card = tk.Frame(self.frame, bg="white", bd=2, relief="ridge")
        self.quote_card.pack(pady=10, padx=10, fill="x", expand=False)

        self.quote_label = tk.Label(
            self.quote_card, text="", wraplength=420, font=("Segoe UI", 13, "italic"),
            justify="center", bg="white", fg="#444", padx=20, pady=20
        )
        self.quote_label.pack()

        # Navigation buttons
        btn_frame = tk.Frame(self.frame, bg="#f0f2f5")
        btn_frame.pack(pady=20)

        self.prev_btn = tk.Button(
            btn_frame, text="← Previous", command=self.prev_quote,
            font=("Segoe UI", 10, "bold"), bg="#0078d7", fg="white",
            activebackground="#005fa3", activeforeground="white",
            padx=14, pady=6, relief="flat", cursor="hand2"
        )
        self.prev_btn.grid(row=0, column=0, padx=10)

        self.next_btn = tk.Button(
            btn_frame, text="Next →", command=self.next_quote,
            font=("Segoe UI", 10, "bold"), bg="#0078d7", fg="white",
            activebackground="#005fa3", activeforeground="white",
            padx=14, pady=6, relief="flat", cursor="hand2"
        )
        self.next_btn.grid(row=0, column=1, padx=10)

        # Back button
        self.back_btn = tk.Button(
            self.frame, text="⏎ Back to Main Menu", command=self.back_to_main,
            font=("Segoe UI", 10, "bold"), bg="#e0e0e0", fg="#333",
            activebackground="#ccc", activeforeground="#000",
            padx=14, pady=6, relief="flat", cursor="hand2"
        )
        self.back_btn.pack(pady=(10, 5))

        self.load_quotes()
        self.index = 0
        if self.quotes:
            self.show_quote()
        else:
            self.quote_label.config(text="No quotes found. Please contact the admin.")

    def load_quotes(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT quote_text FROM quotes ORDER BY id")
        self.quotes = [row[0] for row in cursor.fetchall()]
        conn.close()

    def show_quote(self):
        self.quote_label.config(text=f'"{self.quotes[self.index]}"')

    def next_quote(self):
        if self.quotes:
            self.index = (self.index + 1) % len(self.quotes)
            self.show_quote()

    def prev_quote(self):
        if self.quotes:
            self.index = (self.index - 1) % len(self.quotes)
            self.show_quote()

    def back_to_main(self):
        self.frame.destroy()
        self.root.title("Main Menu")
        from modules.main_menu import MainMenu
        MainMenu(self.root, getattr(self.root, 'current_user', 'User'))
