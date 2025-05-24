import tkinter as tk
from tkinter import messagebox, ttk
from modules.database import get_connection

class AdminManageQuotes:
    def __init__(self, root):
        self.root = root
        self.root.title("Manage Motivational Quotes")
        self.root.configure(bg="#121212")
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        # Card frame
        self.card = tk.Frame(root, bg="#1E1E2F")
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=550, height=550)

        # Title Label
        self.title_label = tk.Label(self.card, text="Manage Motivational Quotes",
                                    fg="#BB86FC", bg="#1E1E2F",
                                    font=("Segoe UI", 20, "bold"))
        self.title_label.pack(pady=(20, 15))

        # Treeview frame for quotes + scrollbar
        tree_frame = tk.Frame(self.card, bg="#1E1E2F")
        tree_frame.pack(fill="both", expand=True, padx=20)

        columns = ("seq", "quote")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=10)
        self.tree.heading("seq", text="#")
        self.tree.heading("quote", text="Quote")
        self.tree.column("seq", width=35, anchor='center')  # Reduced width here
        self.tree.column("quote", anchor='w')

        # Style Treeview fonts & colors
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#1E1E2F",
                        foreground="white",
                        rowheight=28,
                        fieldbackground="#1E1E2F",
                        font=("Segoe UI", 12))
        style.configure("Treeview.Heading",
                        font=("Segoe UI", 13, "bold"),
                        background="#121212",
                        foreground="#BB86FC")
        style.map('Treeview', background=[('selected', '#BB86FC')], foreground=[('selected', 'black')])

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')

        # Entry frame for adding new quote
        entry_frame = tk.Frame(self.card, bg="#1E1E2F")
        entry_frame.pack(pady=15, padx=20, fill="x")

        self.new_quote_var = tk.StringVar()
        self.new_quote_entry = tk.Entry(entry_frame, textvariable=self.new_quote_var,
                                        font=("Segoe UI", 12))
        self.new_quote_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))

        self.add_button = tk.Button(entry_frame, text="Add Quote",
                                    bg="#BB86FC", fg="black", font=("Segoe UI", 12, "bold"),
                                    relief="flat", cursor="hand2",
                                    activebackground="#9a6de0",
                                    command=self.add_quote)
        self.add_button.pack(side='left')
        self.add_button.bind("<Enter>", lambda e: self.add_button.config(bg="#9a6de0"))
        self.add_button.bind("<Leave>", lambda e: self.add_button.config(bg="#BB86FC"))

        # Buttons frame for Delete, Back to Admin
        btn_frame = tk.Frame(self.card, bg="#1E1E2F")
        btn_frame.pack(fill='x', pady=15, padx=20)

        self.delete_button = tk.Button(btn_frame, text="Delete Selected Quote",
                                       bg="#CF6679", fg="black", font=("Segoe UI", 12, "bold"),
                                       relief="flat", cursor="hand2",
                                       activebackground="#b24d5b",
                                       command=self.delete_quote)
        self.delete_button.pack(side='left', padx=(0, 10))
        self.delete_button.bind("<Enter>", lambda e: self.delete_button.config(bg="#b24d5b"))
        self.delete_button.bind("<Leave>", lambda e: self.delete_button.config(bg="#CF6679"))

        self.back_button = tk.Button(btn_frame, text="Back to Admin Menu",
                                     bg="#03DAC6", fg="black", font=("Segoe UI", 12, "bold"),
                                     relief="flat", cursor="hand2",
                                     activebackground="#02b8a4",
                                     command=self.back_to_admin)
        self.back_button.pack(side='left')
        self.back_button.bind("<Enter>", lambda e: self.back_button.config(bg="#02b8a4"))
        self.back_button.bind("<Leave>", lambda e: self.back_button.config(bg="#03DAC6"))

        self.load_quotes()

    def load_quotes(self):
        self.tree.delete(*self.tree.get_children())
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, quote_text FROM quotes ORDER BY id")
        self.quotes = cursor.fetchall()
        conn.close()

        for i, q in enumerate(self.quotes, start=1):
            self.tree.insert("", "end", values=(i, q[1]))

    def add_quote(self):
        quote_text = self.new_quote_var.get().strip()
        if not quote_text:
            messagebox.showwarning("Empty input", "Please enter a quote before adding.")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO quotes (quote_text) VALUES (?)", (quote_text,))
            conn.commit()
            conn.close()
            self.new_quote_var.set("")
            self.load_quotes()
            messagebox.showinfo("Success", "Quote added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add quote: {e}")

    def delete_quote(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a quote to delete.")
            return

        item = selected[0]
        index = self.tree.index(item)
        quote_id = self.quotes[index][0]
        quote_text = self.quotes[index][1]

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this quote?\n\n\"{quote_text}\"")
        if not confirm:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM quotes WHERE id=?", (quote_id,))
            conn.commit()
            conn.close()
            self.load_quotes()
            messagebox.showinfo("Deleted", "Quote deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete quote: {e}")

    def back_to_admin(self):
        self.card.destroy()
        self.root.title("Admin Main Menu")
        from modules.admin_main_menu import AdminMainMenu
        AdminMainMenu(self.root)
