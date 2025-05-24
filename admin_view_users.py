import tkinter as tk
from tkinter import ttk, messagebox
from modules.database import get_connection

class AdminViewUsers:
    def __init__(self, root):
        self.root = root
        self.root.configure(bg="#121212")
        self.root.title("View Users")

        self.frame = tk.Frame(root, bg="#121212")
        self.frame.pack(padx=20, pady=20, fill='both', expand=True)

        tk.Label(self.frame, text="👥 All Registered Users", font=("Segoe UI", 16, "bold"),
                 fg="#BB86FC", bg="#121212").pack(pady=10)

        # Treeview frame
        tree_frame = tk.Frame(self.frame, bg="#1E1E2F", bd=2, relief="flat")
        tree_frame.pack(fill='both', expand=True, padx=10, pady=10)

        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview",
                        background="#1E1E2F",
                        foreground="#FFFFFF",
                        rowheight=25,
                        fieldbackground="#1E1E2F",
                        font=("Segoe UI", 11))
        style.configure("Treeview.Heading",
                        background="#03DAC6",
                        foreground="black",
                        font=("Segoe UI", 12, "bold"))

        style.map("Treeview",
                  background=[("selected", "#BB86FC")],
                  foreground=[("selected", "black")])

        columns = ("id", "username")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings', selectmode='browse')
        self.tree.heading("id", text="User ID")
        self.tree.heading("username", text="Username")
        self.tree.column("id", width=80, anchor='center')
        self.tree.column("username", width=240, anchor='w')

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')

        self.load_users()

        # Buttons frame
        btn_frame = tk.Frame(self.frame, bg="#121212")
        btn_frame.pack(pady=15)

        btn_font = ("Segoe UI", 10, "bold")  # Slightly smaller font
        btn_width = 18  # Reduced width

        self.delete_button = tk.Button(
            btn_frame,
            text="🗑️  Delete Selected",
            font=btn_font,
            bg="#CF6679",
            fg="black",
            activebackground="#b24d5b",
            relief="flat",
            cursor="hand2",
            width=btn_width,
            compound="left",
            padx=6,
            command=self.delete_user
        )
        self.delete_button.grid(row=0, column=0, padx=(0, 8), ipadx=6, ipady=5)
        self.delete_button.bind("<Enter>", lambda e: self.delete_button.config(bg="#b24d5b"))
        self.delete_button.bind("<Leave>", lambda e: self.delete_button.config(bg="#CF6679"))

        self.back_button = tk.Button(
            btn_frame,
            text="⬅️  Back to Menu",
            font=btn_font,
            bg="#03DAC6",
            fg="black",
            activebackground="#02b8a4",
            relief="flat",
            cursor="hand2",
            width=btn_width,
            compound="left",
            padx=6,
            command=self.back_to_admin
        )
        self.back_button.grid(row=0, column=1, padx=(8, 0), ipadx=6, ipady=5)
        self.back_button.bind("<Enter>", lambda e: self.back_button.config(bg="#02b8a4"))
        self.back_button.bind("<Leave>", lambda e: self.back_button.config(bg="#03DAC6"))



    def load_users(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username FROM users ORDER BY id")
        users = cursor.fetchall()
        conn.close()

        for user in users:
            self.tree.insert('', 'end', values=user)

    def delete_user(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a user to delete.")
            return

        user_id = self.tree.item(selected[0])['values'][0]
        username = self.tree.item(selected[0])['values'][1]

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user '{username}'?")
        if not confirm:
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
            cursor.execute("DELETE FROM moods WHERE user_id=?", (user_id,))

            conn.commit()
            conn.close()

            messagebox.showinfo("Deleted", f"User '{username}' has been deleted.")
            self.load_users()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete user: {e}")

    def back_to_admin(self):
        self.frame.destroy()
        self.root.title("Admin Main Menu")
        from modules.admin_main_menu import AdminMainMenu
        AdminMainMenu(self.root)
