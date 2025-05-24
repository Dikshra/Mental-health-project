import tkinter as tk

class MainMenu:
    def __init__(self, root, username):
        self.root = root
        self.username = username
        self.root.title("Main Menu - User")
        self.root.configure(bg="#121212")  # dark background
        self.root.geometry("400x400")
        self.root.resizable(False, False)

        # Card frame
        self.card = tk.Frame(root, bg="#1E1E2F")
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=350, height=350)

        # Welcome label
        self.welcome_label = tk.Label(self.card, text=f"Welcome, {self.username}!",
                                      fg="#BB86FC", bg="#1E1E2F",
                                      font=("Segoe UI", 20, "bold"))
        self.welcome_label.pack(pady=(30, 25))

        # Buttons container
        self.btn_frame = tk.Frame(self.card, bg="#1E1E2F")
        self.btn_frame.pack(pady=5, fill="x", padx=40)

        # Button styles
        btn_font = ("Segoe UI", 13, "bold")
        btn_bg = "#BB86FC"
        btn_active_bg = "#9a6de0"
        btn_fg = "black"
        btn_pad_y = 12

        # Mood Detector Button
        self.btn_mood = tk.Button(self.btn_frame, text="Mood Detector",
                                  bg=btn_bg, fg=btn_fg, font=btn_font,
                                  relief="flat", cursor="hand2",
                                  activebackground=btn_active_bg,
                                  command=self.mood_detector)
        self.btn_mood.pack(fill="x", pady=8)
        self.btn_mood.bind("<Enter>", lambda e: self.btn_mood.config(bg=btn_active_bg))
        self.btn_mood.bind("<Leave>", lambda e: self.btn_mood.config(bg=btn_bg))

        # Motivate Me Button (teal)
        self.btn_motivate = tk.Button(self.btn_frame, text="Motivate Me",
                                     bg="#03DAC6", fg="black", font=btn_font,
                                     relief="flat", cursor="hand2",
                                     activebackground="#02b8a4",
                                     command=self.motivate_me)
        self.btn_motivate.pack(fill="x", pady=8)
        self.btn_motivate.bind("<Enter>", lambda e: self.btn_motivate.config(bg="#02b8a4"))
        self.btn_motivate.bind("<Leave>", lambda e: self.btn_motivate.config(bg="#03DAC6"))

        # Mental Health Report Button (purple)
        self.btn_report = tk.Button(self.btn_frame, text="Mental Health Report",
                                    bg=btn_bg, fg=btn_fg, font=btn_font,
                                    relief="flat", cursor="hand2",
                                    activebackground=btn_active_bg,
                                    command=self.health_report)
        self.btn_report.pack(fill="x", pady=8)
        self.btn_report.bind("<Enter>", lambda e: self.btn_report.config(bg=btn_active_bg))
        self.btn_report.bind("<Leave>", lambda e: self.btn_report.config(bg=btn_bg))

        # Logout Button (red)
        self.btn_logout = tk.Button(self.btn_frame, text="Logout",
                                    bg="#CF6679", fg="black", font=btn_font,
                                    relief="flat", cursor="hand2",
                                    activebackground="#b24d5b",
                                    command=self.logout)
        self.btn_logout.pack(fill="x", pady=8)
        self.btn_logout.bind("<Enter>", lambda e: self.btn_logout.config(bg="#b24d5b"))
        self.btn_logout.bind("<Leave>", lambda e: self.btn_logout.config(bg="#CF6679"))

    def mood_detector(self):
        self.card.destroy()
        self.root.title("Mood Detector")
        from modules.mood_detector import MoodDetector
        MoodDetector(self.root, self.username)

    def motivate_me(self):
        self.card.destroy()
        self.root.title("Motivate Me")
        from modules.motivate_me import MotivateMe
        MotivateMe(self.root)

    def health_report(self):
        self.card.destroy()
        self.root.title("Mental Health Report")
        from modules.health_report import HealthReport
        HealthReport(self.root, self.username)

    def logout(self):
        self.card.destroy()
        self.root.title("Login")
        from modules.login import LoginWindow
        LoginWindow(self.root)
