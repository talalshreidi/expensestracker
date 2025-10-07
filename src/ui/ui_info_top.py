import tkinter as tk
from styles import AppStyles

# UI Component for displaying main information at the top of the window
# App Title on Left
# Balance figure on right side live updating

class InfoTop(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.configure(bg=AppStyles.BG_SECONDARY, relief="solid", bd=1)
        self.create_widgets()

    def create_widgets(self):
        # Main container with padding
        container = tk.Frame(self, bg=AppStyles.BG_SECONDARY)
        container.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Left side - App title and status
        left_frame = tk.Frame(container, bg=AppStyles.BG_SECONDARY)
        left_frame.pack(side="left", fill="y")
        
        self.title_label = tk.Label(left_frame, 
                                  text="💰 Expense Tracker", 
                                  font=AppStyles.FONT_TITLE,
                                  bg=AppStyles.BG_SECONDARY,
                                  fg=AppStyles.PRIMARY_COLOR)
        self.title_label.pack(anchor="w")

        self.filter_status_label = tk.Label(left_frame, 
                                          text="", 
                                          font=AppStyles.FONT_SMALL,
                                          bg=AppStyles.BG_SECONDARY,
                                          fg=AppStyles.ACCENT_COLOR)
        self.filter_status_label.pack(anchor="w", pady=(5, 0))

        # Right side - Balance display with styling
        right_frame = tk.Frame(container, bg=AppStyles.BG_SECONDARY)
        right_frame.pack(side="right", fill="y")
        
        balance_container = tk.Frame(right_frame, 
                                   bg=AppStyles.BG_ACCENT, 
                                   relief="solid", 
                                   bd=1)
        balance_container.pack(padx=10, pady=5)
        
        balance_title = tk.Label(balance_container, 
                               text="Current Balance", 
                               font=AppStyles.FONT_SMALL,
                               bg=AppStyles.BG_ACCENT,
                               fg=AppStyles.TEXT_SECONDARY)
        balance_title.pack(pady=(8, 2))
        
        self.balance_label = tk.Label(balance_container, 
                                    text="$0.00", 
                                    font=("Segoe UI", 20, "bold"),
                                    bg=AppStyles.BG_ACCENT,
                                    fg=AppStyles.PRIMARY_COLOR)
        self.balance_label.pack(pady=(0, 10), padx=15)

    def update_balance(self, new_balance):
        # Color code the balance
        color = AppStyles.INCOME_COLOR if new_balance >= 0 else AppStyles.SUCCESS_COLOR
        self.balance_label.config(text=f"${new_balance:.2f}", fg=color)

    def set_filter_status(self, is_filtered):
        if is_filtered:
            self.filter_status_label.config(text="🔍 Filtered View Active")
        else:
            self.filter_status_label.config(text="")