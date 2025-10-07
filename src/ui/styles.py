# Color scheme and styling constants
class AppStyles:
    # Color palette
    PRIMARY_COLOR = "#2E86AB"      # Blue
    SECONDARY_COLOR = "#A23B72"    # Purple
    ACCENT_COLOR = "#F18F01"       # Orange
    SUCCESS_COLOR = "#C73E1D"      # Red for expenses
    INCOME_COLOR = "#2D5016"       # Green for income
    
    # Background colors
    BG_PRIMARY = "#F5F7FA"         # Light gray-blue
    BG_SECONDARY = "#FFFFFF"       # White
    BG_ACCENT = "#E8F4F8"          # Very light blue
    
    # Text colors
    TEXT_PRIMARY = "#2C3E50"       # Dark blue-gray
    TEXT_SECONDARY = "#7F8C8D"     # Medium gray
    TEXT_LIGHT = "#FFFFFF"         # White
    
    # Fonts
    FONT_TITLE = ("Segoe UI", 18, "bold")
    FONT_HEADING = ("Segoe UI", 12, "bold")
    FONT_BODY = ("Segoe UI", 10)
    FONT_SMALL = ("Segoe UI", 9)
    
    # Button styles
    BUTTON_PRIMARY = {
        'bg': PRIMARY_COLOR,
        'fg': TEXT_LIGHT,
        'font': FONT_BODY,
        'relief': 'flat',
        'padx': 15,
        'pady': 8,
        'cursor': 'hand2'
    }
    
    BUTTON_SECONDARY = {
        'bg': BG_SECONDARY,
        'fg': TEXT_PRIMARY,
        'font': FONT_BODY,
        'relief': 'solid',
        'bd': 1,
        'padx': 12,
        'pady': 6,
        'cursor': 'hand2'
    }
    
    BUTTON_DANGER = {
        'bg': SUCCESS_COLOR,
        'fg': TEXT_LIGHT,
        'font': FONT_BODY,
        'relief': 'flat',
        'padx': 15,
        'pady': 8,
        'cursor': 'hand2'
    }
    
    # Entry styles
    ENTRY_STYLE = {
        'font': FONT_BODY,
        'relief': 'solid',
        'bd': 1,
        'highlightthickness': 2,
        'highlightcolor': PRIMARY_COLOR
    }