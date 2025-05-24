import tkinter as tk

class AdminMainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Main Menu")
        self.root.configure(bg="#121212")
        self.root.geometry("400x400")
        self.root.resizable(False, False)

        # Card-style container
        self.card = tk.Frame(root, bg="#1E1E2F")
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=350, height=350)

        # Welcome message
        tk.Label(
            self.card,
            text="👨‍💼 Welcome, Admin!",
            fg="#FF5555",
            bg="#1E1E2F",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=(30, 25))

        # Button frame
        self.btn_frame = tk.Frame(self.card, bg="#1E1E2F")
        self.btn_frame.pack(pady=5, fill="x", padx=40)

        # Common button style
        btn_font = ("Segoe UI", 13, "bold")
        btn_fg = "black"
        btn_pad_y = 12

        # View Users Button
        self.btn_users = tk.Button(
            self.btn_frame, text="👥 View All Users", font=btn_font,
            bg="#BB86FC", fg=btn_fg, relief="flat", cursor="hand2",
            activebackground="#9a6de0", command=self.view_users
        )
        self.btn_users.pack(fill="x", pady=8)
        self.btn_users.bind("<Enter>", lambda e: self.btn_users.config(bg="#9a6de0"))
        self.btn_users.bind("<Leave>", lambda e: self.btn_users.config(bg="#BB86FC"))

        # Manage Quotes Button
        self.btn_quotes = tk.Button(
            self.btn_frame, text="💬 Manage Quotes", font=btn_font,
            bg="#03DAC6", fg=btn_fg, relief="flat", cursor="hand2",
            activebackground="#02b8a4", command=self.manage_quotes
        )
        self.btn_quotes.pack(fill="x", pady=8)
        self.btn_quotes.bind("<Enter>", lambda e: self.btn_quotes.config(bg="#02b8a4"))
        self.btn_quotes.bind("<Leave>", lambda e: self.btn_quotes.config(bg="#03DAC6"))

        # View Reports Button
        self.btn_reports = tk.Button(
            self.btn_frame, text="📊 View Reports", font=btn_font,
            bg="#BB86FC", fg=btn_fg, relief="flat", cursor="hand2",
            activebackground="#9a6de0", command=self.view_reports
        )
        self.btn_reports.pack(fill="x", pady=8)
        self.btn_reports.bind("<Enter>", lambda e: self.btn_reports.config(bg="#9a6de0"))
        self.btn_reports.bind("<Leave>", lambda e: self.btn_reports.config(bg="#BB86FC"))

        # Logout Button
        self.btn_logout = tk.Button(
            self.btn_frame, text="🚪 Logout", font=btn_font,
            bg="#CF6679", fg=btn_fg, relief="flat", cursor="hand2",
            activebackground="#b24d5b", command=self.logout
        )
        self.btn_logout.pack(fill="x", pady=8)
        self.btn_logout.bind("<Enter>", lambda e: self.btn_logout.config(bg="#b24d5b"))
        self.btn_logout.bind("<Leave>", lambda e: self.btn_logout.config(bg="#CF6679"))

    def view_users(self):
        self.card.destroy()
        self.root.title("View Users")
        from modules.admin_view_users import AdminViewUsers
        AdminViewUsers(self.root)

    def manage_quotes(self):
        self.card.destroy()
        self.root.title("Manage Quotes")
        from modules.admin_manage_quotes import AdminManageQuotes
        AdminManageQuotes(self.root)

    def view_reports(self):
        self.card.destroy()
        self.root.title("View Reports")
        from modules.admin_view_reports import AdminViewReports
        AdminViewReports(self.root)

    def logout(self):
        self.card.destroy()
        self.root.title("Login")
        from modules.login import LoginWindow
        LoginWindow(self.root)
