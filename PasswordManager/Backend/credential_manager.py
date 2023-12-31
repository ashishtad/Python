
import tkinter as tk
from tkinter import messagebox
from Backend.logger import Logger

class CredentialManager:
    def __init__(self, master, user):
        self.master = master
        self.user = user
        self.logger = Logger()
        self.master.title("Credential Manager")

        # Define credential types
        self.credential_types = [ "Website", "Credit/Debit Card", "Other"]

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
      #StringVar is a variable class in Tkinter to assocaite with widgets
      self.credential_type = tk.StringVar()
      #Default value set to first element of credential_types i.e Website as default value
      self.credential_type.set(self.credential_types[0])
      #Drop down option is created where credential_type is passed to hold the selected dropdown option value.
      #*credential_types unpacks the list and pass each elements as individual argument in list
      credential_type_dropdown = tk.OptionMenu(self.add_credential_window, self.credential_type, *self.credential_types)
      credential_type_dropdown.pack(pady=5)

      self.logger.log_debug(f"Credential Manager: show_add_credential, credential type selected: {self.credential_type}")
      #List to store the labels and it's corresponding entries so as to clear them[ i.e. before /default displayed] when an option is selected
      self.credentials_labels_entries = []
      self.credential_type.trace_add("write",self.update_ui)
                                       
    def update_ui(self, *args):
        selected_type = self.credential_type.get()
        self.logger.log_debug(f"Credential Manager: update_ui type selected : {selected_type}")

        #Clear the label and entries for the previously selected credential type.
        # Clear the already displaying entries/labels then display the corresponding for the selected type.
        self.clear_label_entries(self.credentials_labels_entries)
        # For website or other credential types
        if selected_type == self.credential_types[0] or selected_type == self.credential_types[2]:
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

        # For credit/debit or other credential types
        elif selected_type == self.credential_types[1] :
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