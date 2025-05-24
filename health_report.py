import tkinter as tk
from tkinter import ttk, messagebox
from modules.database import get_connection
from collections import Counter

class HealthReport:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Mental Health Report")

        self.frame = tk.Frame(root, bg="#f0f2f5")
        self.frame.pack(padx=20, pady=20, fill='both', expand=True)

        tk.Label(
            self.frame,
            text=f"{self.username}'s Mental Health Report",
            font=("Segoe UI", 16, "bold"),
            bg="#f0f2f5", fg="#333"
        ).pack(pady=(10, 20))

        # Treeview with custom style
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        rowheight=30,
                        fieldbackground="white",
                        font=("Segoe UI", 11))
        style.configure("Treeview.Heading",
                        font=("Segoe UI", 11, "bold"),
                        background="#0078d7",
                        foreground="white")

        columns = ("date", "mood")
        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings')
        self.tree.heading("date", text="Date")
        self.tree.heading("mood", text="Mood")

        self.tree.column("date", width=150, anchor="center")
        self.tree.column("mood", width=150, anchor="center")

        self.tree.pack(fill='both', expand=True, pady=10)

        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        self.avg_label = tk.Label(
            self.frame, text="", font=("Segoe UI", 13, "italic"),
            bg="#f0f2f5", fg="#444"
        )
        self.avg_label.pack(pady=10)

        self.back_btn = tk.Button(
            self.frame, text="⏎ Back to Main Menu", command=self.back_to_main,
            font=("Segoe UI", 10, "bold"), bg="#e0e0e0", fg="#333",
            activebackground="#ccc", activeforeground="#000",
            padx=14, pady=6, relief="flat", cursor="hand2"
        )
        self.back_btn.pack(pady=(10, 5))

        self.load_reports()

    def load_reports(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE username=?", (self.username,))
        user = cursor.fetchone()
        if not user:
            messagebox.showerror("Error", "User not found.")
            return

        user_id = user[0]

        cursor.execute("SELECT date, mood_result FROM moods WHERE user_id=? ORDER BY date DESC", (user_id,))
        records = cursor.fetchall()
        conn.close()

        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        if not records:
            self.avg_label.config(text="No mood data available.")
            return

        moods = []
        for date_str, mood in records:
            date_only = date_str.split(' ')[0]  # Extract just date
            self.tree.insert('', tk.END, values=(date_only, mood.capitalize()))
            moods.append(mood.lower())

        avg_mood = self.calculate_average_mood(moods)
        self.avg_label.config(text=f"🧠 Average Mood: {avg_mood.capitalize()}")

    def calculate_average_mood(self, moods):
        if not moods:
            return "N/A"
        count = Counter(moods)
        return count.most_common(1)[0][0]

    def back_to_main(self):
        self.frame.destroy()
        self.root.title("Main Menu")
        from modules.main_menu import MainMenu
        MainMenu(self.root, self.username)
