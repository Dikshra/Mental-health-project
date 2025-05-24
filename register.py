import tkinter as tk
from tkinter import messagebox
from modules.database import get_connection
import sqlite3

class RegisterWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("User Registration")

        self.frame = tk.Frame(root)
        self.frame.pack(padx=20, pady=20)

        tk.Label(self.frame, text="Register New User", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self.frame, text="Username:").grid(row=1, column=0, sticky="e", pady=5)
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.grid(row=1, column=1, pady=5)

        tk.Label(self.frame, text="Password:").grid(row=2, column=0, sticky="e", pady=5)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=2, column=1, pady=5)

        tk.Label(self.frame, text="Confirm Password:").grid(row=3, column=0, sticky="e", pady=5)
        self.confirm_password_entry = tk.Entry(self.frame, show="*")
        self.confirm_password_entry.grid(row=3, column=1, pady=5)

        tk.Button(self.frame, text="Register", width=15, command=self.register_user).grid(row=4, column=0, columnspan=2, pady=15)
        tk.Button(self.frame, text="Back to Login", command=self.back_to_login).grid(row=5, column=0, columnspan=2)

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

            # Try inserting the user (will fail if username is not unique)
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
