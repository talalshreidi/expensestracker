# 💰 Expense Tracker

A user-friendly personal finance tracker built with Python and SQLite to help you manage your expenses and income with ease.

## 🎯 What It Does

This application helps you keep track of your financial transactions through an intuitive GUI interface. Whether you're monitoring daily expenses or tracking income sources, this tool provides a comprehensive solution for personal financial management.

## 📸 Screenshots

### Main Dashboard
<img width="1195" height="771" alt="Screenshot 2025-10-07 152740" src="https://github.com/user-attachments/assets/dddc4de4-a8ba-49e4-b611-cb801bee8daf" />

The main interface showing your transaction history with balance tracking and filtering options.

### Add New Entry
<img width="322" height="587" alt="Screenshot 2025-10-07 152723" src="https://github.com/user-attachments/assets/4fd4dfef-c95b-4b29-ae60-ae304f8dba9c">

Simple form to add new income or expense entries with category selection and notes.

### Edit Entry
<img width="317" height="583" alt="Screenshot 2025-10-07 152754" src="https://github.com/user-attachments/assets/9db276d4-956f-4b99-b8bb-75c0e10dc53a" />

Easy-to-use edit form for modifying existing transactions.

### Balance Display (Negative)
<img width="173" height="102" alt="Screenshot 2025-10-07 152819" src="https://github.com/user-attachments/assets/b464b3fc-2531-4130-8b4f-1607ec09264e" />

Real-time balance tracking with color-coded indicators.

### ✨ Key Features

- **📝 Easy Entry Management**: Add and edit expense/income entries with amount, category, date, and notes
- **📊 Visual Dashboard**: View all transactions in a clean, organized table with color-coded entries
- **💹 Real-time Balance**: Automatic calculation of total income, expenses, and current balance
- **🔍 Smart Filtering**: Filter entries by date range, category, or transaction type
- **💾 Reliable Storage**: All data securely stored in a local SQLite database
- **✅ Input Validation**: Built-in validation ensures data accuracy and prevents errors
- **🖥️ Modern GUI**: Beautiful Tkinter interface with professional styling and emojis
- **📤 Export Feature**: Export your data to CSV for external analysis

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- Required packages (install via pip):
    ```bash
    pip install tkcalendar
    ```

### Running the Application
1. Clone or download the project files
2. Navigate to the `src/ui` directory
3. Run the main application:
     ```bash
     python ui.py
     ```

## 📁 Project Structure

```
expensetracker/
├── src/
│   ├── ui/              # User interface components
│   │   ├── ui.py        # Main application entry point
│   │   ├── main_window.py
│   │   ├── ui_forms.py
│   │   └── entry_table.py
│   └── db_helper.py     # Database operations
├── data/                # SQLite database storage
└── README.md
```

## 🎨 Features in Detail

- **Transaction Types**: Support for both income and expense tracking
- **Categories**: Pre-defined categories (Food, Transport, Utilities, etc.) with custom category support
- **Date Management**: Calendar picker for easy date selection
- **Filter System**: Advanced filtering by date range, category, and transaction type
- **Balance Tracking**: Live balance updates with color-coded display
- **Data Export**: CSV export functionality for backup and analysis

## 🛠️ Technical Details

- **Frontend**: Python Tkinter with custom styling
- **Database**: SQLite for local data storage
- **Date Handling**: tkcalendar for enhanced date picking
- **Architecture**: Modular design with separated UI components and database layer

Enjoy tracking your finances! 📈

