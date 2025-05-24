import tkinter as tk
from tkinter import messagebox
from modules.database import get_connection

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#121212")  # dark background for contrast
        self.root.geometry("400x350")
        self.root.resizable(False, False)

        # Main card frame (white background, padding, rounded corners simulation)
        self.card = tk.Frame(root, bg="#1E1E2F", bd=0)
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=350, height=300)

        # Title label
        self.title_label = tk.Label(self.card, text="Welcome Back", fg="#BB86FC",
                                    bg="#1E1E2F", font=("Segoe UI", 24, "bold"))
        self.title_label.pack(pady=(30, 20))

        # Username entry with label
        self.username_label = tk.Label(self.card, text="Username", fg="#FFFFFF",
                                       bg="#1E1E2F", font=("Segoe UI", 11))
        self.username_label.pack(anchor="w", padx=40)
        self.username_entry = tk.Entry(self.card, bg="#2A2A3E", fg="white",
                                       relief="flat", font=("Segoe UI", 12))
        self.username_entry.pack(fill="x", padx=40, pady=(0, 15))
        self.username_entry.config(insertbackground='white')

        # Password entry with label
        self.password_label = tk.Label(self.card, text="Password", fg="#FFFFFF",
                                       bg="#1E1E2F", font=("Segoe UI", 11))
        self.password_label.pack(anchor="w", padx=40)
        self.password_entry = tk.Entry(self.card, show="*", bg="#2A2A3E", fg="white",
                                       relief="flat", font=("Segoe UI", 12))
        self.password_entry.pack(fill="x", padx=40, pady=(0, 25))
        self.password_entry.config(insertbackground='white')

        # Buttons frame
        self.btn_frame = tk.Frame(self.card, bg="#1E1E2F")
        self.btn_frame.pack(fill="x", padx=40)

        # Login Button (flat, purple)
        self.login_button = tk.Button(self.btn_frame, text="Login",
                                      bg="#BB86FC", fg="black",
                                      activebackground="#9a6de0",
                                      font=("Segoe UI", 12, "bold"),
                                      relief="flat", cursor="hand2",
                                      command=self.login)
        self.login_button.pack(side="left", fill="x", expand=True, pady=10, padx=(0,10))
        self.login_button.bind("<Enter>", lambda e: self.login_button.config(bg="#9a6de0"))
        self.login_button.bind("<Leave>", lambda e: self.login_button.config(bg="#BB86FC"))

        # Create User Button (flat, teal)
        self.create_user_button = tk.Button(self.btn_frame, text="Create User",
                                            bg="#03DAC6", fg="black",
                                            activebackground="#02b8a4",
                                            font=("Segoe UI", 12, "bold"),
                                            relief="flat", cursor="hand2",
                                            command=self.create_user)
        self.create_user_button.pack(side="left", fill="x", expand=True, pady=10)
        self.create_user_button.bind("<Enter>", lambda e: self.create_user_button.config(bg="#02b8a4"))
        self.create_user_button.bind("<Leave>", lambda e: self.create_user_button.config(bg="#03DAC6"))

        # Set focus on username field
        self.username_entry.focus()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            messagebox.showinfo("Login Success", "Welcome, Admin!")
            self.card.destroy()
            from modules.admin_main_menu import AdminMainMenu
            AdminMainMenu(self.root)
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                messagebox.showinfo("Login Success", f"Welcome, {username}!")
                self.card.destroy()
                from modules.main_menu import MainMenu
                MainMenu(self.root, username)
            else:
                messagebox.showerror("Login Failed", "Invalid credentials.")
        except Exception as e:
            messagebox.showerror("Database Error", f"Error accessing database:\n{e}")

    def create_user(self):
        self.card.destroy()
        from modules.register import RegisterWindow
        RegisterWindow(self.root)
