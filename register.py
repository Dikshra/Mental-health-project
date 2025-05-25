import tkinter as tk
from tkinter import messagebox
from modules.database import get_connection
import sqlite3

class RegisterWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("User Registration")
        self.root.configure(bg="#1e1e1e")  # Dark background

        self.frame = tk.Frame(root, bg="#1e1e1e")
        self.frame.pack(padx=40, pady=30)

        label_style = {"bg": "#1e1e1e", "fg": "#ffffff", "font": ("Arial", 12)}
        entry_style = {"bg": "#2c2c2c", "fg": "#ffffff", "insertbackground": "white", "highlightthickness": 1, "highlightbackground": "#555555"}
        button_style = {"bg": "#3c3f41", "fg": "#ffffff", "activebackground": "#5c5f61", "activeforeground": "#ffffff", "relief": "flat"}

        tk.Label(self.frame, text="Register New User", font=("Arial", 16, "bold"), bg="#1e1e1e", fg="#00ffff").grid(row=0, column=0, columnspan=2, pady=(0, 20))

        tk.Label(self.frame, text="Username:", **label_style).grid(row=1, column=0, sticky="e", pady=5)
        self.username_entry = tk.Entry(self.frame, **entry_style)
        self.username_entry.grid(row=1, column=1, pady=5, ipady=3, ipadx=3)

        tk.Label(self.frame, text="Password:", **label_style).grid(row=2, column=0, sticky="e", pady=5)
        self.password_entry = tk.Entry(self.frame, show="*", **entry_style)
        self.password_entry.grid(row=2, column=1, pady=5, ipady=3, ipadx=3)

        tk.Label(self.frame, text="Confirm Password:", **label_style).grid(row=3, column=0, sticky="e", pady=5)
        self.confirm_password_entry = tk.Entry(self.frame, show="*", **entry_style)
        self.confirm_password_entry.grid(row=3, column=1, pady=5, ipady=3, ipadx=3)

        register_btn = tk.Button(self.frame, text="Register", width=20, command=self.register_user, **button_style)
        register_btn.grid(row=4, column=0, columnspan=2, pady=(15, 10))

        back_btn = tk.Button(self.frame, text="Back to Login", width=20, command=self.back_to_login, **button_style)
        back_btn.grid(row=5, column=0, columnspan=2)

    def register_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()

        if not username or not password or not confirm_password:
            messagebox.showwarning("Input Error", "All fields are required.")
            return

        if password != confirm_password:
            messagebox.showerror("Password Error", "Passwords do not match.")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully!")
            self.back_to_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Registration Error", "Username already exists.")
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
        finally:
            conn.close()

    def back_to_login(self):
        self.frame.destroy()
        from modules.login import LoginWindow
        self.root.title("Login")
        LoginWindow(self.root)
