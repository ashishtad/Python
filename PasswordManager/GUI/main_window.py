#######################################
# GUI for password manager
# Author: Ashish Tad
#######################################

import tkinter as tk
from tkinter import messagebox
from Backend.authentication import Authentication
from Backend.logger import Logger
from Backend.credential_manager import CredentialManager


class PasswordManagerApp:
    def __init__(self,master):

        self.authentication = Authentication()
        self.logger = Logger()
               
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
        user_info = self.authentication.retrieve_userInfo(username)
        if user_info:
            stored_hashed_password, salt = user_info
            #Hash the eneterd password 
            entered_hashed_password = self.authentication.hash_password(password,salt)

            if entered_hashed_password == stored_hashed_password:
                messagebox.showinfo("Login", "Login Successful!!")
                #Now open the credential manager window upon successful login
                self.open_credential_manager(username)
            else:
                messagebox.showerror("Login", "Invalid username or Password")
        else:
            messagebox.showerror("Login", "Invalid username or Password")


    def Signup(self, new_username, new_password):
        #placeholder for signup functionality
        #Implement to store new username and password securely
     
        salt = self.authentication.generate_salt()
        hashed_password = self.authentication.hash_password(new_password,salt)
        #Check if user already exists
        user_info = self.authentication.retrieve_userInfo(new_username)
        #Exiting user update the DB entry
        if user_info:
            self.authentication.update_user(new_username,hashed_password,salt)
        #New user
        else:
            self.authentication.store_user(new_username,hashed_password,salt)
        messagebox.showinfo("Signup", "Account created successfully!!")


    def open_credential_manager(self,logged_in_user):
        self.logger.log_info(f"Opening credential manager for {logged_in_user}")
        #Open a new credential Manager window
        credential_manager_window = tk.Toplevel(self.master)
        credential_manager_window.title("Credential Manager")

        #Create instance of credential manager app
        credential_manager_app = CredentialManager(credential_manager_window,logged_in_user)

        


        

