import tkinter
from main_window import MainWindow

def create_main_window():
    # Ensure tkinter is working
    root = tkinter.Tk()
    root.withdraw()  # Hide the default root window
    
    # Create the main application window
    app = MainWindow()
    
    # Ensure it's visible
    app.deiconify()
    app.lift()
    app.focus_force()
    
    return app

if __name__ == "__main__":
    try:
        app = create_main_window()
        print("Application window created. Starting main loop...")
        app.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()