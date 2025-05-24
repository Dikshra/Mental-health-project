import tkinter as tk
from tkinter import messagebox
import json
import datetime
from modules.database import get_connection

class ScrollableFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        canvas = tk.Canvas(self, borderwidth=0, background="#fafafa")
        self.frame = tk.Frame(canvas, background="#fafafa")
        scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        canvas.create_window((0, 0), window=self.frame, anchor="nw")

        self.frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        self.canvas = canvas

class MoodDetector:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Mood Detector")

        self.questions = self.load_questions()
        self.current_question_index = 0
        self.answers = []

        # Layout: Top = Scrollable content, Bottom = fixed Next button
        self.wrapper = tk.Frame(root, bg="#f0f2f5")
        self.wrapper.pack(expand=True, fill="both", padx=20, pady=20)

        # Scrollable section
        self.scrollable_frame = ScrollableFrame(self.wrapper)
        self.scrollable_frame.pack(side="top", expand=True, fill="both")

        self.frame = self.scrollable_frame.frame

        self.question_label = tk.Label(
            self.frame, text="", font=("Segoe UI", 14, "bold"),
            wraplength=440, justify="left", fg="#333", bg="#fafafa"
        )
        self.question_label.pack(anchor="w", pady=(0, 20))

        self.var = tk.IntVar(value=-1)
        self.option_buttons = []
        for i in range(5):
            rb = tk.Radiobutton(
                self.frame, text="", variable=self.var, value=i,
                font=("Segoe UI", 12), anchor="w",
                padx=10, pady=8,
                bg="#ffffff", activebackground="#d0f0fd",
                selectcolor="#87ceeb"
            )
            rb.pack(fill="x", pady=5)
            self.option_buttons.append(rb)

        # Fixed button section
        self.button_frame = tk.Frame(self.wrapper, bg="#f0f2f5")
        self.button_frame.pack(side="bottom", fill="x", pady=(10, 0))

        self.next_button = tk.Button(
            self.button_frame, text="Next", command=self.next_question,
            font=("Segoe UI", 12, "bold"),
            bg="#0078d7", fg="white", activebackground="#005a9e",
            relief="flat", padx=15, pady=8
        )
        self.next_button.pack(anchor="e", padx=10)

        self.load_next_question()

    def load_questions(self):
        with open("assets/questions.json", "r") as file:
            return json.load(file)

    def load_next_question(self):
        if self.current_question_index < len(self.questions):
            self.var.set(-1)
            q = self.questions[self.current_question_index]
            self.question_label.config(text=f"Q{self.current_question_index + 1}: {q['question']}")

            for i, option in enumerate(q['options']):
                self.option_buttons[i].config(text=option['text'], value=i)
                self.option_buttons[i].pack(fill="x", pady=5)

            for j in range(len(q['options']), 5):
                self.option_buttons[j].pack_forget()

            self.scrollable_frame.canvas.yview_moveto(0)
        else:
            self.finish_quiz()

    def next_question(self):
        selected_index = self.var.get()
        if selected_index == -1:
            messagebox.showwarning("No selection", "Please select an option.")
            return

        current_question = self.questions[self.current_question_index]
        selected_score = current_question['options'][selected_index]['score']
        self.answers.append(selected_score)

        self.current_question_index += 1
        self.load_next_question()

    def finish_quiz(self):
        total_score = sum(self.answers)
        mood = self.get_mood_from_score(total_score)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE username=?", (self.username,))
        user = cursor.fetchone()
        user_id = user[0] if user else None

        if user_id:
            cursor.execute("INSERT INTO moods (user_id, date, mood_result) VALUES (?, ?, ?)",
                           (user_id, datetime.datetime.now().strftime("%Y-%m-%d"), mood))
            conn.commit()
        conn.close()

        messagebox.showinfo("Mood Detected", f"Your mood is: {mood}")
        self.wrapper.destroy()
        from modules.main_menu import MainMenu
        MainMenu(self.root, self.username)

    def get_mood_from_score(self, score):
        if score <= 100:
            return "Sad"
        elif score <= 200:
            return "Neutral"
        else:
            return "Happy"
