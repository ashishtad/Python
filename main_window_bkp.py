#######################################
# GUI for password manager
# Author: Ashish Tad
#######################################

import tkinter as tk
from tkinter import messagebox
import os
import hashlib #Module provides common interface to multiple secure hashing algorithms.
import sqlite3
import logging
import datetime

LOG_DIRECTORY = './Log'

class PasswordManagerApp:
    def __init__(self,master):

        if not os.path.exists(LOG_DIRECTORY):
            os.makedirs(LOG_DIRECTORY)
        #Generate time stamp for the log file name
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
        log_file_name = f'{LOG_DIRECTORY}/password_manager_{timestamp}.log'

        logging.basicConfig(filename=log_file_name,level=logging.DEBUG)
               
        #Initialize the main window
        self.master = master
        self.master.title("Password Manager")

        #create and place widgets
        self.label = tk.Label(master,text="Welcome to Password Manager!!")
        self.label.pack(pady=100)
        #Login button functionality
        self.login_button = tk.Button(master,text="Login",command=self.show_login_window)
        self.login_button.pack(side=tk.LEFT,padx=5)

        #signup button functionality
        self.signup_button = tk.Button(master,text="Signup",command=self.show_signup_window)
        self.signup_button.pack(side=tk.LEFT,padx=5)

        #quit button. This will quit the tkinter master window
        self.quit_button = tk.Button(master,text="Quit",command=master.quit)
        self.quit_button.pack(pady=5)

        #Initialise data base
        self.init_database()

    def init_database(self):
        #Initiate a connection to sqlite DB and an iterator to iterate over DB
        try:
            self.connection = sqlite3.connect("password_manager.db")
            self.cursor = self.connection.cursor()

            #Create the usertable if not exists
            #''' closing triplets allow the SQL statement to span multiple lines for better readability.
            self.cursor.execute('''
                                CREATE TABLE IF NOT EXISTS users (
                                username TEXT PRIMARY KEY,
                                hashed_password TEXT,
                                salt TEXT
                                )
                                
                                ''')
            #commit the changes and close the connection
            self.connection.commit()
        except sqlite3.Err as e:
            logging.error(f"Error in init Database: {e}")
    
    def close_database(self):
        try:
            self.connection.close()
        except sqlite3.Error as e:
            logging.error(f"Error in closing database connection: {e}")

    def show_login_window(self):
        
        login_window = tk.Toplevel(self.master)
        login_window.title("Login")
        #Labels
        tk.Label(login_window, text="Username:").pack(pady=5)
        username_entry = tk.Entry(login_window)
        username_entry.pack(pady=5)

        tk.Label(login_window, text="Password:").pack(pady=5)
        password_entry = tk.Entry(login_window, show="*")
        password_entry.pack(pady=10)

        #Login Button
        login_button = tk.Button(login_window,text="Login", command=lambda: self.login(username_entry.get(),password_entry.get()))
        login_button.pack()

    def show_signup_window(self):
        signup_window = tk.Toplevel(self.master)
        signup_window.title("Signup")

        #Labels
        tk.Label(signup_window, text="Enter Username").pack(pady=5)
        new_username_entry = tk.Entry(signup_window)
        new_username_entry.pack(pady=5)

        tk.Label(signup_window, text = "Enter password").pack(pady=5)
        new_password_entry = tk.Entry(signup_window, show="*")
        new_password_entry.pack(pady=10)

        #Signup Button
        signup_button = tk.Button(signup_window, text="Signup", command=lambda: self.Signup(new_username_entry.get(), new_password_entry.get()))
        signup_button.pack()


    def login(self,username,password):
        #Placeholder for login functionality

        #Retrieve the user from password_manager database users table
        user_info = self.retrieve_userInfo(username)
        if user_info:
            stored_hashed_password, salt = user_info
            #Hash the eneterd password 
            entered_hashed_password = self.hash_password(password,salt)

            if entered_hashed_password == stored_hashed_password:
                messagebox.showinfo("Login", "Login Successful!!")
            else:
                messagebox.showerror("Login", "Invalid username or Password")
        else:
            messagebox.showerror("Login", "Invalid username or Password")


    def retrieve_userInfo(self,username):
        try:
            self.cursor.execute('SELECT hashed_password, salt FROM users WHERE username = ?',(username,))
            #Fetch the result (one row ) from the query
            user_info = self.cursor.fetchone()
            return user_info
        except sqlite3.Error as e:
            logging.error(f"Error retrieveing the user information: {e}")
            return None



    def Signup(self, new_username, new_password):
        #placeholder for signup functionality
        #Implement to store new username and password securely
     
        salt = self.generate_salt()
        hashed_password = self.hash_password(new_password,salt)
        #Check if user already exists
        user_info = self.retrieve_userInfo(new_username)
        #Exiting user update the DB entry
        if user_info:
            self.update_user(new_username,hashed_password,salt)
        #New user
        else:
            self.store_user(new_username,hashed_password,salt)
        messagebox.showinfo("Signup", "Account created successfully!!")


    def update_user(self,username,hash_password,salt):
        try:
            self.cursor.execute('UPDATE users SET hashed_password = ?, salt = ? WHERE username = ?',
                                (hash_password,salt,username))
            self.connection.commit()
        except sqlite3.Error as e:
            logging.error(f"Error in storing user in database: {e}")

    #Store the user account details sqlite DB
    def store_user(self,username,hashed_password,salt):
        try:
            self.cursor.execute('INSERT INTO users VALUES(?, ?, ?)',(username,hashed_password,salt))
            self.connection.commit()
        except sqlite3.Error as e:
            logging.error(f"Error in storing user to database! {e}")
        

    # Generate random salt or random number of specified length
    def generate_salt( self,length = 16):
        #urandom generates a random number of 16bytes which is converted to hex
        return os.urandom(length).hex()
    
    #Return a sha256 hashed password
    def hash_password(self,password,salt):
        #This combines the plain text password and salt, then encode it as hashlib sha256 API expects bytes to be hashed.
        #hexdigest represents the hexadecimal representation of hashed password
        hashed_password = hashlib.sha256((password+salt).encode('utf-8')).hexdigest()
        return hashed_password
        


def main():
    #create the main tkinter window
    # variable root now holds the reference to the main window
    root = tk.Tk()
    #Instantiate the PasswordManagerApp class.
    #Passing root associates the app i.e PasswordManager class with Tkinter main window
    app = PasswordManagerApp(root) 
    # Close the database when the window is closed
    root.protocol("WM_DELETE_WINDOW", app.close_database)
    #call the mainloop of Tk.
    # The mainloop function is a method provided by Tkinter that runs the application, handling events such as button clicks, keypresses, etc
    root.mainloop()


if __name__ == "__main__":
    main()

