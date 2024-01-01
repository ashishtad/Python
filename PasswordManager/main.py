import tkinter as tk
from GUI.main_window import PasswordManagerApp
from Backend.database import Database

def main():
    #create the main tkinter window
    # variable root now holds the reference to the main window
    root = tk.Tk()
    database = Database()
    #Instantiate the PasswordManagerApp class.
    #Passing root associates the app i.e PasswordManager class with Tkinter main window
    app = PasswordManagerApp(root) 
    # Close the database when the window is closed
    root.protocol("WM_DELETE_WINDOW", database.close_database())
    #call the mainloop of Tk.
    # The mainloop function is a method provided by Tkinter that runs the application, handling events such as button clicks, keypresses, etc
    root.mainloop()


if __name__ == "__main__":
    main()