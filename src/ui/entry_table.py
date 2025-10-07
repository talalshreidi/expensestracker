# Entry Table for displaying expenses
import tkinter as tk
from tkinter import ttk
from styles import AppStyles


class EntryTable(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg=AppStyles.BG_SECONDARY)
        self.entry_ids = {}
        self.create_widgets()
        self.configure_styles()

    def configure_styles(self):
        """Configure enhanced table styling"""
        style = ttk.Style()
        
        # Configure Treeview
        style.configure('Enhanced.Treeview',
                       background=AppStyles.BG_SECONDARY,
                       foreground=AppStyles.TEXT_PRIMARY,
                       fieldbackground=AppStyles.BG_SECONDARY,
                       font=AppStyles.FONT_BODY,
                       rowheight=30)
        
        # Configure headings
        style.configure('Enhanced.Treeview.Heading',
                       background=AppStyles.PRIMARY_COLOR,
                       foreground=AppStyles.TEXT_LIGHT,
                       font=AppStyles.FONT_HEADING,
                       relief="flat")
        
        # Configure selection colors
        style.map('Enhanced.Treeview',
                 background=[('selected', AppStyles.ACCENT_COLOR)],
                 foreground=[('selected', AppStyles.TEXT_PRIMARY)])

    def create_widgets(self):
        # Table title
        title_frame = tk.Frame(self, bg=AppStyles.BG_SECONDARY)
        title_frame.pack(fill="x", pady=(0, 10))
        
        table_title = tk.Label(title_frame, 
                             text="📋 Transaction History", 
                             font=AppStyles.FONT_HEADING,
                             bg=AppStyles.BG_SECONDARY,
                             fg=AppStyles.TEXT_PRIMARY)
        table_title.pack(anchor="w")
        
        # Table container
        table_container = tk.Frame(self, bg=AppStyles.BG_SECONDARY)
        table_container.pack(fill="both", expand=True)
        
        # Define columns
        self.columns = ["Date", "Type", "Category", "Note", "Amount"]
        
        # Create the Treeview with enhanced styling
        self.table = ttk.Treeview(table_container, 
                                 columns=self.columns, 
                                 show="headings",
                                 style='Enhanced.Treeview')
        
        # Configure columns with better widths
        column_widths = {"Date": 120, "Type": 80, "Category": 120, "Note": 200, "Amount": 100}
        
        for col in self.columns:
            self.table.heading(col, text=f"  {col}", anchor="w")
            self.table.column(col, width=column_widths.get(col, 120), anchor="w")
        
        # Right-align amount column
        self.table.column("Amount", anchor="e")
        
        # Scrollbar with styling
        scrollbar_frame = tk.Frame(table_container, bg=AppStyles.BG_SECONDARY)
        scrollbar_frame.pack(side="right", fill="y")
        
        self.scrollbar = ttk.Scrollbar(scrollbar_frame, 
                                      orient="vertical", 
                                      command=self.table.yview)
        self.table.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack widgets
        self.table.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(fill="y")
        
        # Configure selection
        self.table.configure(selectmode="browse")

    def clear_table(self):
        for item in self.table.get_children():
            self.table.delete(item)
        self.entry_ids.clear()  # Clear the ID mapping

    def get_selected_entry(self):
        selected = self.table.selection()
        if selected:
            return self.table.item(selected[0])['values']
        return None
    
    def add_entry(self, entries):
        self.clear_table()
        for i, entry in enumerate(entries):
            # Color code based on type
            amount_text = f"${entry[4]:.2f}"
            if entry[2] == "Income":
                amount_color = "income"
            else:
                amount_color = "expense"
            
            formatted_entry = (
                entry[1],  # date
                f"{'💰' if entry[2] == 'Income' else '💸'} {entry[2]}",  # type with emoji
                f"🏷️ {entry[3]}",  # category with emoji
                entry[5] or "",  # note
                amount_text  # amount
            )
            
            # Insert with tags for coloring
            item = self.table.insert("", "end", values=formatted_entry, tags=(amount_color,))
            self.entry_ids[item] = entry[0]
        
        # Configure tags for row coloring
        self.table.tag_configure('income', 
                               background='#E8F5E8', 
                               foreground=AppStyles.INCOME_COLOR)
        self.table.tag_configure('expense', 
                               background='#FFE8E8', 
                               foreground=AppStyles.SUCCESS_COLOR)

    def get_selected_entry_id(self):
        """Get the ID of the selected entry."""
        selected = self.table.selection()
        if selected:
            return self.entry_ids.get(selected[0])
        return None

    def get_selected_entry_data(self):
        """Get the full data of the selected entry from database."""
        entry_id = self.get_selected_entry_id()
        if entry_id:
            # Import here to avoid circular imports
            import sys
            import os
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            from db_helper import db
            return db.get_entry_by_id(entry_id)
        return None

    def bind_double_click(self, callback):
        self.table.bind("<Double-1>", callback)

    def bind_selection_change(self, callback):
        self.table.bind("<<TreeviewSelect>>", callback)



