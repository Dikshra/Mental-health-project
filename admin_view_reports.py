import tkinter as tk
from tkinter import ttk, messagebox
from modules.database import get_connection
import datetime

class AdminViewReports:
    def __init__(self, root):
        self.root = root
        self.root.geometry("900x600")
        self.root.title("View Mood Detector Reports")
        self.root.configure(bg="#1E1E1E")  # Dark background

        style = ttk.Style(self.root)
        style.theme_use('clam')

        # Frame styles - dark background
        style.configure("Main.TFrame", background="#1E1E1E")
        style.configure("Filter.TFrame", background="#1E1E1E")

        # Label style - light text on dark background
        style.configure("TLabel", background="#1E1E1E", foreground="#FFFFFF", font=("Segoe UI", 12))

        # Entry style - dark background, white text, subtle border
        style.configure("TEntry",
                        fieldbackground="#2D2D30",
                        foreground="#FFFFFF",
                        padding=5,
                        borderwidth=1,
                        relief="solid")

        # Combobox style same as entry
        style.configure("TCombobox",
                        fieldbackground="#2D2D30",
                        background="#2D2D30",
                        foreground="#FFFFFF",
                        padding=5,
                        borderwidth=1,
                        relief="solid")

        # Button style: dark blue background with hover effect
        style.configure("TButton",
                        background="#0A64A0",
                        foreground="white",
                        font=("Segoe UI", 11),
                        padding=8,
                        borderwidth=0)
        style.map('TButton',
                  background=[('active', '#004C87')],
                  foreground=[('active', 'white')])

        # Treeview style
        style.configure("Treeview",
                        background="#252526",
                        foreground="white",
                        fieldbackground="#252526",
                        font=("Segoe UI", 11))
        style.map("Treeview", background=[('selected', '#0A64A0')], foreground=[('selected', 'white')])

        # Treeview heading style (dark gray background)
        style.configure("Treeview.Heading",
                        background="#3C3C3C",
                        foreground="white",
                        font=("Segoe UI", 12, "bold"))

        # Main frame
        self.frame = ttk.Frame(root, style="Main.TFrame", padding=20)
        self.frame.pack(fill='both', expand=True)

        title_label = ttk.Label(self.frame, text="View Mood Detector Reports", font=("Segoe UI", 18, "bold"))
        title_label.pack(pady=(0, 15))

        # Filters Frame
        filter_frame = ttk.Frame(self.frame, style="Filter.TFrame")
        filter_frame.pack(fill='x', pady=(0, 10))

        # Row 0
        ttk.Label(filter_frame, text="User:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.user_filter = ttk.Combobox(filter_frame, state="readonly", width=20)
        self.user_filter.grid(row=0, column=1, sticky='w', padx=5, pady=5)

        ttk.Label(filter_frame, text="Start Date (YYYY-MM-DD):").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.start_date_entry = ttk.Entry(filter_frame, width=20)
        self.start_date_entry.grid(row=0, column=3, sticky='w', padx=5, pady=5)

        # Row 1
        ttk.Label(filter_frame, text="End Date (YYYY-MM-DD):").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.end_date_entry = ttk.Entry(filter_frame, width=20)
        self.end_date_entry.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        self.filter_button = ttk.Button(filter_frame, text="Filter", width=15, command=self.apply_filters)
        self.filter_button.grid(row=1, column=2, sticky='w', padx=10, pady=5)

        self.reset_button = ttk.Button(filter_frame, text="Reset", width=15, command=self.reset_filters)
        self.reset_button.grid(row=1, column=3, sticky='w', padx=5, pady=5)

        # Treeview
        columns = ("username", "date", "mood_result")
        self.tree = ttk.Treeview(self.frame, columns=columns, show='headings', style='Treeview')
        self.tree.heading("username", text="Username")
        self.tree.heading("date", text="Date")
        self.tree.heading("mood_result", text="Mood")

        self.tree.column("username", width=280, anchor='center')
        self.tree.column("date", width=160, anchor='center')
        self.tree.column("mood_result", width=160, anchor='center')

        self.tree.pack(fill='both', expand=True, pady=10)

        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        self.back_button = ttk.Button(self.frame, text="Back to Admin Menu", width=25, command=self.back_to_admin)
        self.back_button.pack(pady=15)

        self.load_users()
        self.load_reports()

    def load_users(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users ORDER BY username")
        users = [row[0] for row in cursor.fetchall()]
        conn.close()

        self.user_filter['values'] = ['All'] + users
        self.user_filter.current(0)

    def load_reports(self, username=None, start_date=None, end_date=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()

        query = """
            SELECT u.username, m.date, m.mood_result
            FROM moods m
            JOIN users u ON m.user_id = u.id
        """
        conditions = []
        params = []

        if username and username != 'All':
            conditions.append("u.username = ?")
            params.append(username)

        if start_date:
            conditions.append("date(m.date) >= date(?)")
            params.append(start_date)

        if end_date:
            conditions.append("date(m.date) <= date(?)")
            params.append(end_date)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY m.date DESC"

        cursor.execute(query, params)
        reports = cursor.fetchall()
        conn.close()

        for report in reports:
            username, date_str, mood = report
            date_fmt = date_str.split(' ')[0] if date_str else ''
            self.tree.insert('', tk.END, values=(username, date_fmt, mood))

    def apply_filters(self):
        username = self.user_filter.get()
        start_date = self.start_date_entry.get().strip()
        end_date = self.end_date_entry.get().strip()

        for dt in [start_date, end_date]:
            if dt:
                try:
                    datetime.datetime.strptime(dt, "%Y-%m-%d")
                except ValueError:
                    messagebox.showerror("Invalid Date", f"Date '{dt}' is not in valid YYYY-MM-DD format.")
                    return

        self.load_reports(username=username, start_date=start_date or None, end_date=end_date or None)

    def reset_filters(self):
        self.user_filter.current(0)
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)
        self.load_reports()

    def back_to_admin(self):
        self.frame.destroy()
        self.root.title("Admin Main Menu")
        from modules.admin_main_menu import AdminMainMenu
        AdminMainMenu(self.root)
