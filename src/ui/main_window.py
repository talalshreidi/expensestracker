import tkinter
import sys
import os
import tkinter.messagebox 
import csv
from tkinter import filedialog, ttk
from datetime import datetime
from tkcalendar import DateEntry

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui_info_top import InfoTop
from ui_forms import AddForm, EditForm
from entry_table import EntryTable
from db_helper import db
from styles import AppStyles  # Import the styles

class MainWindow(tkinter.Tk):

    def __init__(self):
        super().__init__()
        self.title("💰 Expense Tracker")
        self.geometry("1200x750")
        self.configure(bg=AppStyles.BG_PRIMARY)
        
        # Configure style for ttk widgets
        self.style = ttk.Style()
        self.configure_ttk_styles()
        
        # Force window to be visible and on top
        self.lift()
        self.attributes('-topmost', True)
        self.after_idle(self.attributes, '-topmost', False)

        # Create main container with padding
        self.main_container = tkinter.Frame(self, bg=AppStyles.BG_PRIMARY)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=15)

        # Top Info Area
        self.info_top = InfoTop(self.main_container)
        self.info_top.pack(side="top", fill="x", pady=(0, 15))

        # Filters Frame with styled background
        self.filters_container = tkinter.Frame(self.main_container, bg=AppStyles.BG_SECONDARY, relief="solid", bd=1)
        self.filters_container.pack(side="top", fill="x", pady=(0, 15))
        
        self.filters_frame = tkinter.Frame(self.filters_container, bg=AppStyles.BG_SECONDARY)
        self.filters_frame.pack(fill="x", padx=15, pady=12)
        self.create_filters_frame()

        # Table container with border
        self.table_container = tkinter.Frame(self.main_container, bg=AppStyles.BG_SECONDARY, relief="solid", bd=1)
        self.table_container.pack(expand=True, fill="both", pady=(0, 15))
        
        # Center Table Area
        self.entry_table = EntryTable(self.table_container)
        self.entry_table.pack(expand=True, fill="both", padx=10, pady=10)

        self.entry_table.bind_double_click(self.on_row_double_click)
        
        # Buttons Frame at Bottom with better styling
        self.buttons_container = tkinter.Frame(self.main_container, bg=AppStyles.BG_PRIMARY)
        self.buttons_container.pack(side="bottom", fill="x")
        
        self.buttons_frame = tkinter.Frame(self.buttons_container, bg=AppStyles.BG_PRIMARY)
        self.buttons_frame.pack(anchor="center")
        self.create_action_buttons()

        # Load data after UI is created
        self.after(100, self.refresh_data)

    def configure_ttk_styles(self):
        """Configure ttk widget styles"""
        # Configure Combobox style
        self.style.configure('Custom.TCombobox',
                           fieldbackground=AppStyles.BG_SECONDARY,
                           background=AppStyles.BG_SECONDARY,
                           foreground=AppStyles.TEXT_PRIMARY,
                           arrowcolor=AppStyles.PRIMARY_COLOR)
        
        # Configure Treeview style
        self.style.configure('Custom.Treeview',
                           background=AppStyles.BG_SECONDARY,
                           foreground=AppStyles.TEXT_PRIMARY,
                           fieldbackground=AppStyles.BG_SECONDARY,
                           font=AppStyles.FONT_BODY)
        
        self.style.configure('Custom.Treeview.Heading',
                           background=AppStyles.PRIMARY_COLOR,
                           foreground=AppStyles.TEXT_LIGHT,
                           font=AppStyles.FONT_HEADING)

    def create_action_buttons(self):
        """Create styled action buttons"""
        self.add_button = tkinter.Button(self.buttons_frame, 
                                       text="➕ Add Entry", 
                                       command=self.open_add_form,
                                       **AppStyles.BUTTON_PRIMARY)
        self.add_button.pack(side="left", padx=8)

        self.edit_button = tkinter.Button(self.buttons_frame, 
                                        text="✏️ Edit Entry", 
                                        command=self.open_edit_form,
                                        **AppStyles.BUTTON_SECONDARY)
        self.edit_button.pack(side="left", padx=8)

        self.delete_button = tkinter.Button(self.buttons_frame, 
                                          text="🗑️ Delete", 
                                          command=self.delete_entry,
                                          **AppStyles.BUTTON_DANGER)
        self.delete_button.pack(side="left", padx=8)

    def create_filters_frame(self):
        # Title for filters section
        filter_title = tkinter.Label(self.filters_frame, 
                                   text="📊 Filters & Export", 
                                   font=AppStyles.FONT_HEADING,
                                   bg=AppStyles.BG_SECONDARY,
                                   fg=AppStyles.TEXT_PRIMARY)
        filter_title.pack(anchor="w", pady=(0, 8))
        
        # Main filters row
        filters_row = tkinter.Frame(self.filters_frame, bg=AppStyles.BG_SECONDARY)
        filters_row.pack(fill="x")
        
        # Left side - Filters
        filters_left = tkinter.Frame(filters_row, bg=AppStyles.BG_SECONDARY)
        filters_left.pack(side="left", fill="x", expand=True)

        # Date Range Filter with styled labels
        date_label = tkinter.Label(filters_left, 
                                 text="📅 From:", 
                                 font=AppStyles.FONT_BODY,
                                 bg=AppStyles.BG_SECONDARY,
                                 fg=AppStyles.TEXT_PRIMARY)
        date_label.pack(side="left", padx=(0, 5))
        
        self.from_date_entry = DateEntry(filters_left, 
                                        width=12, 
                                        background=AppStyles.PRIMARY_COLOR,
                                        foreground='white', 
                                        borderwidth=1,
                                        font=AppStyles.FONT_BODY,
                                        date_pattern='mm-dd-yyyy')
        self.from_date_entry.pack(side="left", padx=(0, 15))

        to_label = tkinter.Label(filters_left, 
                               text="📅 To:", 
                               font=AppStyles.FONT_BODY,
                               bg=AppStyles.BG_SECONDARY,
                               fg=AppStyles.TEXT_PRIMARY)
        to_label.pack(side="left", padx=(0, 5))
        
        self.to_date_entry = DateEntry(filters_left, 
                                      width=12, 
                                      background=AppStyles.PRIMARY_COLOR,
                                      foreground='white', 
                                      borderwidth=1,
                                      font=AppStyles.FONT_BODY,
                                      date_pattern='mm-dd-yyyy')
        self.to_date_entry.pack(side="left", padx=(0, 15))

        # Category Filter
        cat_label = tkinter.Label(filters_left, 
                                text="🏷️ Category:", 
                                font=AppStyles.FONT_BODY,
                                bg=AppStyles.BG_SECONDARY,
                                fg=AppStyles.TEXT_PRIMARY)
        cat_label.pack(side="left", padx=(0, 5))
        
        categories = self.get_categories_safe()
        self.category_filter = ttk.Combobox(filters_left, 
                                           values=categories,
                                           state="readonly",
                                           style='Custom.TCombobox',
                                           font=AppStyles.FONT_BODY,
                                           width=12)
        self.category_filter.set("All")
        self.category_filter.pack(side="left", padx=(0, 15))

        # Type Filter 
        type_label = tkinter.Label(filters_left, 
                                 text="💰 Type:", 
                                 font=AppStyles.FONT_BODY,
                                 bg=AppStyles.BG_SECONDARY,
                                 fg=AppStyles.TEXT_PRIMARY)
        type_label.pack(side="left", padx=(0, 5))
        
        type_options = ["All", "Income", "Expense"]
        self.type_filter = ttk.Combobox(filters_left,
                                       values=type_options,
                                       state="readonly",
                                       style='Custom.TCombobox',
                                       font=AppStyles.FONT_BODY,
                                       width=8)
        self.type_filter.set("All")
        self.type_filter.pack(side="left", padx=(0, 15))

        # Filter Action Buttons
        button_frame = tkinter.Frame(filters_left, bg=AppStyles.BG_SECONDARY)
        button_frame.pack(side="left")
        
        apply_btn_style = AppStyles.BUTTON_PRIMARY.copy()
        apply_btn_style.update({'padx': 12, 'pady': 6})
        
        self.apply_filter_button = tkinter.Button(button_frame, 
                                                text="🔍 Apply", 
                                                command=self.apply_filters,
                                                **apply_btn_style)
        self.apply_filter_button.pack(side="left", padx=3)

        clear_btn_style = AppStyles.BUTTON_SECONDARY.copy()
        clear_btn_style.update({'padx': 12, 'pady': 6})
        
        self.clear_filter_button = tkinter.Button(button_frame, 
                                                text="🔄 Clear", 
                                                command=self.clear_filters,
                                                **clear_btn_style)
        self.clear_filter_button.pack(side="left", padx=3)
        
        self.refresh_categories_button = tkinter.Button(button_frame, 
                                                      text="↻", 
                                                      command=self.refresh_categories, 
                                                      width=3,
                                                      **clear_btn_style)
        self.refresh_categories_button.pack(side="left", padx=3)

        # Right side - Export
        filters_right = tkinter.Frame(filters_row, bg=AppStyles.BG_SECONDARY)
        filters_right.pack(side="right")

        export_btn_style = AppStyles.BUTTON_SECONDARY.copy()
        export_btn_style.update({'bg': AppStyles.ACCENT_COLOR, 'fg': AppStyles.TEXT_LIGHT})
        
        self.export_button = tkinter.Button(filters_right, 
                                          text="📊 Export CSV", 
                                          command=self.export_to_csv,
                                          **export_btn_style)
        self.export_button.pack(side="right")

    def get_categories_safe(self):
        """Safely get categories with fallback."""
        default_categories = ["All", "Food", "Transport", "Utilities", "Entertainment", "Other"]
        
        try:
            db_categories = db.get_all_categories()
            if db_categories:
                # Combine and deduplicate
                all_cats = set(default_categories[1:] + db_categories)
                categories = ["All"] + sorted(list(all_cats))
                return categories
            else:
                return default_categories
        except:
            return default_categories

    def refresh_categories(self):
        """Refresh the category filter dropdown with current database categories."""
        current_selection = self.category_filter.get()
        
        # Get updated categories
        categories = self.get_categories_safe()
        
        # Update the combobox values
        self.category_filter['values'] = categories
        
        # Restore selection if it still exists
        if current_selection in categories:
            self.category_filter.set(current_selection)
        else:
            self.category_filter.set("All")

    def apply_filters(self):
        """Apply filters to the table display."""
        from_date = self.from_date_entry.get()
        to_date = self.to_date_entry.get()
        category = self.category_filter.get()
        entry_type = self.type_filter.get()

        print(f"Debug - Applying filters: category={category}, type={entry_type}")

        # Get filtered entries from database
        entries = db.get_filtered_entries(from_date, to_date, category, entry_type)
        self.entry_table.add_entry(entries)

        # Update balance based on filtered data
        total_income, total_expense, balance = db.get_filtered_totals(from_date, to_date, category, entry_type)
        self.info_top.update_balance(balance)
        self.info_top.set_filter_status(True)

        # Visual feedback is automatic with Combobox - no need to update manually!



    def clear_filters(self):
        """Clear all filters and show all data."""
        today = datetime.now().date()
        self.from_date_entry.set_date(today)
        self.to_date_entry.set_date(today)
        
        # Clear dropdowns - visual feedback is automatic with Combobox
        self.category_filter.set("All")
        self.type_filter.set("All")
        
        self.info_top.set_filter_status(False)
        self.refresh_data()

    def export_to_csv(self):
        """Export current table data to CSV file."""
        try:
            entries = db.get_all_entries()
            
            if not entries:
                tkinter.messagebox.showinfo("No Data", "No entries to export.")
                return

            filename = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Save CSV file"
            )

            if filename:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['ID', 'Date', 'Type', 'Category', 'Amount', 'Note', 'Created At'])
                    for entry in entries:
                        writer.writerow(entry)

                tkinter.messagebox.showinfo("Export Successful", f"Data exported to {filename}")

        except Exception as e:
            tkinter.messagebox.showerror("Export Error", f"Failed to export data: {str(e)}")

    def open_add_form(self):
        dialog = AddForm(self, root_window=self)
        self.wait_window(dialog)
        if dialog.result:
            db.add_entry(dialog.result)
            self.refresh_data()
            self.refresh_categories()

    def open_edit_form(self):
        entry_data = self.entry_table.get_selected_entry_data()
        if entry_data:
            dialog = EditForm(self, entry_data=entry_data)
            self.wait_window(dialog)
            if dialog.result:
                db.update_entry(entry_data[0], dialog.result)
                self.refresh_data()
                self.refresh_categories()
        else:
            tkinter.messagebox.showwarning("No Selection", "Please select an entry to edit.")

    def delete_entry(self):
        entry_data = self.entry_table.get_selected_entry_data()
        if entry_data:
            result = tkinter.messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entry?")
            if result:
                db.delete_entry(entry_data[0])
                self.refresh_data()
                self.refresh_categories()
        else:
            tkinter.messagebox.showwarning("No Selection", "Please select an entry to delete.")

    def on_row_double_click(self, event):
        self.open_edit_form()
    
    def refresh_data(self):
        entries = db.get_all_entries()
        self.entry_table.add_entry(entries)
        total_income, total_expense, balance = db.get_totals()
        self.info_top.update_balance(balance)