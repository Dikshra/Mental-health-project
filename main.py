import os
import tkinter as tk
from tkinter import messagebox
from modules.database import initialize_database
from modules.login import LoginWindow

APP_TITLE = "Mental Health Support App"

def main():
    # Ensure 'assets' folder exists
    if not os.path.exists("assets"):
        os.makedirs("assets")

    # Initialize or create SQLite database
    try:
        initialize_database()
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to initialize database.\n\n{e}")
        return

    # Launch Tkinter main window
    root = tk.Tk()
    root.title(APP_TITLE)

    # Set a reasonable default size for Login window
    window_width = 480
    window_height = 480

    # Center window on screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coord = int((screen_width / 2) - (window_width / 2))
    y_coord = int((screen_height / 2) - (window_height / 2))
    root.geometry(f"{window_width}x{window_height}+{x_coord}+{y_coord}")

    # Set minsize for login window (optional)
    root.minsize(480, 480)

    root.resizable(True, True)

    default_font = ("Segoe UI", 10)
    root.option_add("*Font", default_font)
    root.configure(bg="#f0f2f5")

    icon_path = os.path.join("assets", "app_icon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)

    # Show login page
    app = LoginWindow(root)

    root.mainloop()

if __name__ == "__main__":
    main()
