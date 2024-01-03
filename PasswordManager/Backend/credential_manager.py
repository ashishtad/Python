
import tkinter as tk
from tkinter import messagebox
from Backend.logger import Logger
from  Backend.database import Database
from tkinter import messagebox 
from cryptography.fernet import Fernet
import json
import base64

class CredentialManager:
    def __init__(self, master, user):
        self.master = master
        self.user = user
        self.logger = Logger()
        self.database = Database()
        self.master.title("Credential Manager")

        # Define credential types
        self.credential_types = [ "", "Website", "Credit/Debit Card", "Other"]
        # Generate a key for Fernet symmetric encryption
        self.key = Fernet.generate_key()
        #Creating an instance of Fernet class from cryptography library. 
        #This is used for symetric encryption where same key is used for encryption and decryption as well
        self.cipher_suite = Fernet(self.key)

        # Create the main menu of credential manager
        self.create_main_menu() 

    def create_main_menu(self):
        # Clear existing widgets
        self.clear_window()
        tk.Label(self.master, text=f"Welcome, {self.user}!").pack(pady=20)
        # Add buttons for different actions in the main menu
        tk.Button(self.master, text="Add Credential", command=self.show_add_credential).pack(pady=10)
        tk.Button(self.master, text="View Credentials", command=self.show_view_credentials).pack(pady=10)
        # Add logout button
        tk.Button(self.master, text="Logout", command=self.logout).pack(pady=10)

    def show_add_credential(self):
        # Placeholder for showing the add credential window
        messagebox.showinfo("Add Credential", "This will show the add credential window.")

    def show_view_credentials(self):
        # Placeholder for showing the view credentials window
        messagebox.showinfo("View Credentials", "This will show the view credentials window.")

    def show_add_credential(self):
      #placeholder for add credentials
      self.logger.log_debug("Credential Manager: show_add_credential")
      self.add_credential_window = tk.Toplevel(self.master)
      self.add_credential_window.title("Add Credential")

      tk.Label(self.add_credential_window,text = "Credential Type:").pack(pady=5)
      #StringVar is a variable class in Tkinter to associate with widgets.
      #This stringVar class is associated with a callback method in our context update_ui() which will be called when variable (self.credential_type) is read/written
      self.credential_type = tk.StringVar()
      #Default value set to first element of credential_types i.e Website as default value.
      self.credential_type.set(self.credential_types[0])
      #Drop down option is created where credential_type is passed to hold the selected dropdown option value.
      #*credential_types unpacks the list and pass each elements as individual argument in list
      credential_type_dropdown = tk.OptionMenu(self.add_credential_window, self.credential_type, *self.credential_types)
      credential_type_dropdown.pack(pady=5)

      #List to store the labels and it's corresponding entries so as to clear them[ i.e. before /default displayed] when an option is selected
      self.credentials_labels_entries = []
      # flag to track the creation of save button
      self.save_button_created = False
      # Tuple to hold the credential values entered 
      self.credential_values = ()
      #update_ui is the callback method to be called upon update of the drop down options i.e. self.credential_type.
      #trace_add is the method to register this callback
      self.credential_type.trace_add("write",self.update_ui)

     

    def save_credentials(self):
        self.logger.log_debug("Credential Manager: Save credentials")
        #Get the credential type first based on that do the task
        credential_type = self.credential_values[0]
        #For credential type website or other
        if credential_type == self.credential_types[1] or credential_type == self.credential_types[3]:
            self.save_website_credentials(credential_type)
        elif credential_type == self.credential_types[2]:
            self.save_card_crdentials(credential_type)

    def save_website_credentials(self, credential_type):
        self.logger.log_debug(f"Credential Manager: save_website_credentials credential type {credential_type}")
        #Get the credentials from Entry widgets labels
        website_name = self.credential_values[1].get()
        username = self.credential_values[2].get()
        password = self.credential_values[3].get()
        # Create a dictionary to store encrypted credentials.
        #encrypt_data return objects which is not JSON serializable. So approach is to base64 encode the byte data.
        credentials_dict =  {'name': base64.b64encode(self.encrypt_data(website_name)).decode('utf-8'), 
                             'username': base64.b64encode(self.encrypt_data(username)).decode('utf-8'), 
                             'password': base64.b64encode(self.encrypt_data(password)).decode('utf-8')}
        # Convert the dictionary to a JSON string before storing in the database
        encrypted_credentials_json = json.dumps(credentials_dict)
        #Retrieve userid from users table
        select_query = f"SELECT user_id FROM users WHERE username = ?;"
        values = (self.user,)
        if not self.database.execute_query(select_query,values):
            self.logger.log_error(f"save_website_credentials execution Failed for query {select_query}")
            messagebox.showerror("Save", "User id not exits")
        user_info = self.database.cursor.fetchone()
        if user_info:
            userid = user_info[0]
        else:
            messagebox.showerror("Save", "User id not exits")
        
        #Frame query to store the credential in credentials table
        store_query = f"INSERT INTO credentials (user_id, type, encrypted_data) VALUES (?, ?, ?);"
        values = (userid, credential_type, encrypted_credentials_json)
        if not self.database.execute_query(store_query,values):
            self.logger.log_error(f"save_website_credentials execution Failed for query {select_query}")
            messagebox.showerror("Save", "Save credentials Failed!!")
        messagebox.showinfo("Save", "Credentials saved succesfully!!")
        

    def save_card_crdentials(self,credential_type):
        self.logger.log_debug("Credential Manager: save_card_crdentials")


        
    
    #Encrypt the data using fernet symetric encryption
    def encrypt_data(self,data):
        #encode the string to bytes as cryptographic methods work on bytes
        encrypted_data = self.cipher_suite.encrypt(data.encode())
        return encrypted_data


    # Callback method to update the UI for different credential type selected
    def update_ui(self, *args):
        selected_type = self.credential_type.get()
        self.logger.log_debug(f"Credential Manager: update_ui type selected : {selected_type}")

        #Clear the label and entries for the previously selected credential type.
        # Clear the already displaying entries/labels then display the corresponding for the selected type.
        self.clear_label_entries(self.credentials_labels_entries)
        # Destroy the save button if created, so as to create the save button again after the credentials labels are updated 
        if self.save_button_created:
            self.save_button.destroy()
            self.save_button_created = False

        # For website or other credential types
        if selected_type == self.credential_types[1] or selected_type == self.credential_types[3]:
            label1= tk.Label(self.add_credential_window, text="Website Name:")
            label1.pack(pady=5)
            self.credentials_labels_entries.append(label1)
            website_name_entry = tk.Entry(self.add_credential_window)
            website_name_entry.pack(pady=5)
            self.credentials_labels_entries.append(website_name_entry)

            label2 = tk.Label(self.add_credential_window, text="Username")
            label2.pack(pady=5)
            self.credentials_labels_entries.append(label2)
            username_entry = tk.Entry(self.add_credential_window)
            username_entry.pack(pady=5)
            self.credentials_labels_entries.append(username_entry)

            label3 = tk.Label(self.add_credential_window, text="Password")
            label3.pack(pady=5)
            self.credentials_labels_entries.append(label3)
            password_entry = tk.Entry(self.add_credential_window)
            password_entry.pack(pady=5)
            self.credentials_labels_entries.append(password_entry)
            #Pass only the Entry widgets here and the text values, 
            #because the values from the Entry widgets should be extracted only after user enters the value in labels and click save.
            self.credential_values = (selected_type, website_name_entry, username_entry, password_entry)

        # For credit/debit or other credential types
        elif selected_type == self.credential_types[2] :
            label1 = tk.Label(self.add_credential_window, text="Type[Credit/Debit]")
            label1.pack(pady=5)
            self.credentials_labels_entries.append(label1)
            card_type_entry = tk.Entry(self.add_credential_window)
            card_type_entry.pack(pady=5)
            self.credentials_labels_entries.append(card_type_entry)

            label2 = tk.Label(self.add_credential_window, text="Card Number")
            label2.pack(pady=5)
            self.credentials_labels_entries.append(label2)
            card_num_entry = tk.Entry(self.add_credential_window)
            card_num_entry.pack(pady=5)
            self.credentials_labels_entries.append(card_num_entry)

            label3 = tk.Label(self.add_credential_window, text="PIN")
            label3.pack(pady=5)
            self.credentials_labels_entries.append(label3)
            pin_entry = tk.Entry(self.add_credential_window)
            pin_entry.pack(pady=5)
            self.credentials_labels_entries.append(pin_entry)
            #Pass only the Entry widgets here and the text values, 
            #because the values from the Entry widgets should be extracted only after user enters the value in labels and click save.
            self.credential_values = (selected_type, card_type_entry, card_num_entry, pin_entry)
        #Create the save button at the end i.e. after displaying the credential labels
        if not self.save_button_created:
            self.save_button = tk.Button(self.add_credential_window, text="Save", command=self.save_credentials)
            self.save_button.pack(pady=10)
            self.save_button_created = True

    def clear_label_entries(self,credential_label_entries):
        for label_or_entry in credential_label_entries:
            label_or_entry.destroy()
        credential_label_entries.clear()

    def logout(self):
        # Destroy the current credential manager window
        self.master.destroy()

    
    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()