import tkinter as tk
import tkinter.messagebox
from datetime import datetime
from tkcalendar import DateEntry 
from styles import AppStyles

# UI component for displaying forms for adding/editing expenses and income (entry form and edit form)
# Fields: Amount input, Category dropdown, Date picker, Note input

class AddForm(tk.Toplevel):
    def __init__(self, master=None, root_window=None):
        super().__init__(master)
        self.master = master
        self.root_window = root_window

        self.title("💰 Add New Entry")
        self.geometry("450x400")  # Fixed size instead of 350x1000
        self.configure(bg=AppStyles.BG_PRIMARY)
        self.transient(master)
        self.grab_set()

        self.center_window()
        self.result = None
        self.create_widgets()
    
    def create_widgets(self):
        # Main container with padding
        main_frame = tk.Frame(self, bg=AppStyles.BG_PRIMARY)
        main_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, 
                             text="💰 Add New Entry", 
                             font=AppStyles.FONT_TITLE,
                             bg=AppStyles.BG_PRIMARY,
                             fg=AppStyles.PRIMARY_COLOR)
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Form container with background
        form_frame = tk.Frame(main_frame, bg=AppStyles.BG_SECONDARY, relief="solid", bd=1)
        form_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 20))
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Form content with padding
        form_content = tk.Frame(form_frame, bg=AppStyles.BG_SECONDARY)
        form_content.pack(fill="both", padx=20, pady=20)

        # Type selection with styling
        type_label = tk.Label(form_content, 
                            text="💼 Transaction Type:", 
                            font=AppStyles.FONT_BODY,
                            bg=AppStyles.BG_SECONDARY,
                            fg=AppStyles.TEXT_PRIMARY)
        type_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        type_frame = tk.Frame(form_content, bg=AppStyles.BG_SECONDARY)
        type_frame.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 15))
        
        self.type_var = tk.StringVar(value="Expense")
        self.expense_radio = tk.Radiobutton(type_frame, 
                                          text="💸 Expense", 
                                          variable=self.type_var, 
                                          value="Expense",
                                          font=AppStyles.FONT_BODY,
                                          bg=AppStyles.BG_SECONDARY,
                                          fg=AppStyles.TEXT_PRIMARY,
                                          selectcolor=AppStyles.BG_ACCENT)
        self.expense_radio.pack(side="left", padx=(0, 20))
        
        self.income_radio = tk.Radiobutton(type_frame, 
                                         text="💰 Income", 
                                         variable=self.type_var, 
                                         value="Income",
                                         font=AppStyles.FONT_BODY,
                                         bg=AppStyles.BG_SECONDARY,
                                         fg=AppStyles.TEXT_PRIMARY,
                                         selectcolor=AppStyles.BG_ACCENT)
        self.income_radio.pack(side="left")

        # Amount field
        amount_label = tk.Label(form_content, 
                              text="💵 Amount:", 
                              font=AppStyles.FONT_BODY,
                              bg=AppStyles.BG_SECONDARY,
                              fg=AppStyles.TEXT_PRIMARY)
        amount_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        self.amount_entry = tk.Entry(form_content, **AppStyles.ENTRY_STYLE)
        self.amount_entry.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        # Category field
        category_label = tk.Label(form_content, 
                                text="🏷️ Category:", 
                                font=AppStyles.FONT_BODY,
                                bg=AppStyles.BG_SECONDARY,
                                fg=AppStyles.TEXT_PRIMARY)
        category_label.grid(row=4, column=0, sticky="w", pady=(0, 5))
        
        self.category_var = tk.StringVar(self)
        category_frame = tk.Frame(form_content, bg=AppStyles.BG_SECONDARY)
        category_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        self.category_dropdown = tk.OptionMenu(category_frame, self.category_var, 
                                             "Food", "Transport", "Utilities", "Entertainment", "Other")
        self.category_dropdown.config(font=AppStyles.FONT_BODY,
                                    bg=AppStyles.BG_SECONDARY,
                                    fg=AppStyles.TEXT_PRIMARY,
                                    relief="solid",
                                    bd=1)
        self.category_dropdown.pack(fill="x")

        # Other category entry (initially hidden)
        self.other_entry_label = tk.Label(form_content, 
                                        text="📝 Specify Other:", 
                                        font=AppStyles.FONT_BODY,
                                        bg=AppStyles.BG_SECONDARY,
                                        fg=AppStyles.TEXT_PRIMARY)
        self.other_entry = tk.Entry(form_content, **AppStyles.ENTRY_STYLE)
        self.category_var.trace_add("write", lambda *args: self.check_if_other_category(self.category_var.get()))

        # Date field with enhanced DateEntry
        date_label = tk.Label(form_content, 
                            text="📅 Date:", 
                            font=AppStyles.FONT_BODY,
                            bg=AppStyles.BG_SECONDARY,
                            fg=AppStyles.TEXT_PRIMARY)
        date_label.grid(row=6, column=0, sticky="w", pady=(0, 5))
        
        self.date_entry = DateEntry(form_content, 
                                   width=15, 
                                   background=AppStyles.PRIMARY_COLOR,
                                   foreground='white', 
                                   borderwidth=2,
                                   font=AppStyles.FONT_BODY,
                                   date_pattern='mm-dd-yyyy')
        self.date_entry.grid(row=7, column=0, columnspan=2, sticky="w", pady=(0, 15))

        # Note field
        note_label = tk.Label(form_content, 
                            text="📝 Note (Optional):", 
                            font=AppStyles.FONT_BODY,
                            bg=AppStyles.BG_SECONDARY,
                            fg=AppStyles.TEXT_PRIMARY)
        note_label.grid(row=8, column=0, sticky="w", pady=(0, 5))
        
        self.note_entry = tk.Entry(form_content, **AppStyles.ENTRY_STYLE)
        self.note_entry.grid(row=9, column=0, columnspan=2, sticky="ew", pady=(0, 20))

        # Buttons with enhanced styling
        button_frame = tk.Frame(main_frame, bg=AppStyles.BG_PRIMARY)
        button_frame.grid(row=2, column=0, columnspan=3)

        self.submit_button = tk.Button(button_frame, 
                                     text="✅ Add Entry", 
                                     command=self.submit_form,
                                     **AppStyles.BUTTON_PRIMARY)
        self.submit_button.pack(side="left", padx=10)

        cancel_style = AppStyles.BUTTON_SECONDARY.copy()
        self.cancel_button = tk.Button(button_frame, 
                                     text="❌ Cancel", 
                                     command=self.cancel_form,
                                     **cancel_style)
        self.cancel_button.pack(side="left", padx=10)

    def check_if_other_category(self, value):
        if value == "Other":
            self.other_entry_label.grid(row=1, column=2, padx=5, pady=5)
            self.other_entry.grid(row=1, column=3, padx=5, pady=5)
        else:
            self.other_entry_label.grid_forget()
            self.other_entry.grid_forget()

    def submit_form(self):
        # Handle form submission
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                tk.messagebox.showerror("Error", "Amount must be greater than 0.")
                return
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid amount.")
            return
            
        type_val = self.type_var.get()
        category = self.category_var.get()
        if category == "Other":
            category = self.other_entry.get().strip()
            if not category:
                tk.messagebox.showerror("Error", "Please specify the 'Other' category.")
                return

        date = self.date_entry.get()
        note = self.note_entry.get()
        
        if not category or not type_val:
            tk.messagebox.showerror("Error", "Please fill in all required fields.")
            return
        
        self.result = {
            "type": type_val,
            "amount": amount,
            "category": category,
            "date": date,
            "note": note
        }
        self.destroy()

    def cancel_form(self):
        self.result = None
        self.destroy()

    def center_window(self):
        self.update_idletasks()
        # Use consistent sizing
        window_width = 450
        window_height = 400
        x = (self.winfo_screenwidth() // 2) - (window_width // 2)
        y = (self.winfo_screenheight() // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Edit Form Class with enhanced styling
class EditForm(tk.Toplevel):
    def __init__(self, master=None, entry_data=None):
        super().__init__(master)
        self.master = master
        self.entry_data = entry_data
        self.entry_id = entry_data[0] if entry_data else None
        
        self.title("✏️ Edit Entry")
        self.geometry("450x400")  # Increased size to fit all content
        self.configure(bg=AppStyles.BG_PRIMARY)
        self.transient(master)
        self.grab_set()
        
        self.center_window()
        self.result = None
        self.create_widgets()
        self.populate_fields()
    
    def create_widgets(self):
        # Main container with padding
        main_frame = tk.Frame(self, bg=AppStyles.BG_PRIMARY)
        main_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Title
        title_label = tk.Label(main_frame, 
                             text="✏️ Edit Entry", 
                             font=AppStyles.FONT_TITLE,
                             bg=AppStyles.BG_PRIMARY,
                             fg=AppStyles.PRIMARY_COLOR)
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Form container with background
        form_frame = tk.Frame(main_frame, bg=AppStyles.BG_SECONDARY, relief="solid", bd=1)
        form_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 20))
        form_frame.grid_columnconfigure(1, weight=1)
        
        # Form content with padding
        form_content = tk.Frame(form_frame, bg=AppStyles.BG_SECONDARY)
        form_content.pack(fill="both", padx=20, pady=20)
        form_content.grid_columnconfigure(1, weight=1)

        # Type selection with styling
        type_label = tk.Label(form_content, 
                            text="💼 Transaction Type:", 
                            font=AppStyles.FONT_BODY,
                            bg=AppStyles.BG_SECONDARY,
                            fg=AppStyles.TEXT_PRIMARY)
        type_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        type_frame = tk.Frame(form_content, bg=AppStyles.BG_SECONDARY)
        type_frame.grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 15))
        
        self.type_var = tk.StringVar(value="Expense")
        self.expense_radio = tk.Radiobutton(type_frame, 
                                          text="💸 Expense", 
                                          variable=self.type_var, 
                                          value="Expense",
                                          font=AppStyles.FONT_BODY,
                                          bg=AppStyles.BG_SECONDARY,
                                          fg=AppStyles.TEXT_PRIMARY,
                                          selectcolor=AppStyles.BG_ACCENT)
        self.expense_radio.pack(side="left", padx=(0, 20))
        
        self.income_radio = tk.Radiobutton(type_frame, 
                                         text="💰 Income", 
                                         variable=self.type_var, 
                                         value="Income",
                                         font=AppStyles.FONT_BODY,
                                         bg=AppStyles.BG_SECONDARY,
                                         fg=AppStyles.TEXT_PRIMARY,
                                         selectcolor=AppStyles.BG_ACCENT)
        self.income_radio.pack(side="left")

        # Amount field
        amount_label = tk.Label(form_content, 
                              text="💵 Amount:", 
                              font=AppStyles.FONT_BODY,
                              bg=AppStyles.BG_SECONDARY,
                              fg=AppStyles.TEXT_PRIMARY)
        amount_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        self.amount_entry = tk.Entry(form_content, **AppStyles.ENTRY_STYLE)
        self.amount_entry.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 15))

        # Category field
        category_label = tk.Label(form_content, 
                                text="🏷️ Category:", 
                                font=AppStyles.FONT_BODY,
                                bg=AppStyles.BG_SECONDARY,
                                fg=AppStyles.TEXT_PRIMARY)
        category_label.grid(row=4, column=0, sticky="w", pady=(0, 5))
        
        self.category_var = tk.StringVar(self)
        category_frame = tk.Frame(form_content, bg=AppStyles.BG_SECONDARY)
        category_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        self.category_dropdown = tk.OptionMenu(category_frame, self.category_var, 
                                             "Food", "Transport", "Utilities", "Entertainment", "Other")
        self.category_dropdown.config(font=AppStyles.FONT_BODY,
                                    bg=AppStyles.BG_SECONDARY,
                                    fg=AppStyles.TEXT_PRIMARY,
                                    relief="solid",
                                    bd=1)
        self.category_dropdown.pack(fill="x")

        # Other category entry (initially hidden)
        self.other_entry_label = tk.Label(form_content, 
                                        text="📝 Specify Other:", 
                                        font=AppStyles.FONT_BODY,
                                        bg=AppStyles.BG_SECONDARY,
                                        fg=AppStyles.TEXT_PRIMARY)
        self.other_entry = tk.Entry(form_content, **AppStyles.ENTRY_STYLE)
        self.category_var.trace_add("write", lambda *args: self.check_if_other_category(self.category_var.get()))

        # Date field with enhanced DateEntry
        date_label = tk.Label(form_content, 
                            text="📅 Date:", 
                            font=AppStyles.FONT_BODY,
                            bg=AppStyles.BG_SECONDARY,
                            fg=AppStyles.TEXT_PRIMARY)
        date_label.grid(row=6, column=0, sticky="w", pady=(0, 5))
        
        self.date_entry = DateEntry(form_content, 
                                   width=15, 
                                   background=AppStyles.PRIMARY_COLOR,
                                   foreground='white', 
                                   borderwidth=2,
                                   font=AppStyles.FONT_BODY,
                                   date_pattern='mm-dd-yyyy')
        self.date_entry.grid(row=7, column=0, columnspan=2, sticky="w", pady=(0, 15))

        # Note field
        note_label = tk.Label(form_content, 
                            text="📝 Note (Optional):", 
                            font=AppStyles.FONT_BODY,
                            bg=AppStyles.BG_SECONDARY,
                            fg=AppStyles.TEXT_PRIMARY)
        note_label.grid(row=8, column=0, sticky="w", pady=(0, 5))
        
        self.note_entry = tk.Entry(form_content, **AppStyles.ENTRY_STYLE)
        self.note_entry.grid(row=9, column=0, columnspan=2, sticky="ew", pady=(0, 20))

        # Buttons with enhanced styling
        button_frame = tk.Frame(main_frame, bg=AppStyles.BG_PRIMARY)
        button_frame.grid(row=2, column=0, columnspan=3)

        self.submit_button = tk.Button(button_frame, 
                                     text="✅ Update Entry", 
                                     command=self.submit_form,
                                     **AppStyles.BUTTON_PRIMARY)
        self.submit_button.pack(side="left", padx=10)

        cancel_style = AppStyles.BUTTON_SECONDARY.copy()
        self.cancel_button = tk.Button(button_frame, 
                                     text="❌ Cancel", 
                                     command=self.cancel_form,
                                     **cancel_style)
        self.cancel_button.pack(side="left", padx=10)

    def check_if_other_category(self, value):
        if value == "Other":
            self.other_entry_label.grid(row=10, column=0, sticky="w", pady=(0, 5))
            self.other_entry.grid(row=11, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        else:
            self.other_entry_label.grid_forget()
            self.other_entry.grid_forget()

    def submit_form(self):
        # Handle form submission with validation
        try:
            amount = float(self.amount_entry.get())
            if amount <= 0:
                tk.messagebox.showerror("Error", "Amount must be greater than 0.")
                return
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter a valid amount.")
            return

        type_val = self.type_var.get()
        category = self.category_var.get()
        if category == "Other":
            category = self.other_entry.get().strip()
            if not category:
                tk.messagebox.showerror("Error", "Please specify the 'Other' category.")
                return

        date = self.date_entry.get()
        note = self.note_entry.get()
        
        if not category or not type_val:
            tk.messagebox.showerror("Error", "Please fill in all required fields.")
            return
        
        self.result = {
            "type": type_val,
            "amount": amount,
            "category": category,
            "date": date,
            "note": note
        }
        self.destroy()

    def cancel_form(self):
        self.result = None
        self.destroy()

    def center_window(self):
        self.update_idletasks()
        # Calculate center position based on actual window size
        window_width = 450
        window_height = 400
        x = (self.winfo_screenwidth() // 2) - (window_width // 2)
        y = (self.winfo_screenheight() // 2) - (window_height // 2)
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def populate_fields(self):
        """Pre-fill form fields with existing entry data."""
        if self.entry_data:
            self.type_var.set(self.entry_data[2])  # type
            self.amount_entry.insert(0, str(self.entry_data[4]))  # amount
            self.category_var.set(self.entry_data[3])  # category
            
            # Set the date in the DateEntry widget
            try:
                date_obj = datetime.strptime(self.entry_data[1], '%m-%d-%Y').date()
                self.date_entry.set_date(date_obj)
            except ValueError:
                # If date format is different, try other formats or set to today
                self.date_entry.set_date(datetime.now().date())
            
            if self.entry_data[5]:  # note (might be None)
                self.note_entry.insert(0, self.entry_data[5])
            
            # Handle "Other" category
            if self.entry_data[3] not in ["Food", "Transport", "Utilities", "Entertainment"]:
                self.category_var.set("Other")
                self.other_entry.insert(0, self.entry_data[3])
                self.check_if_other_category("Other")
