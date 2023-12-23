
# Credential Manager

import tkinter as tk
from Backend.database import Database
from Backend.logger import Logger

class CredentialManager:
   #Master: credential manager tkinter window passed from main window login functionality
   # user: It's the logged-in user
   def  __init__(self, master, user):
      self.master = master
      self.user = user
      self.master.title("Credential Manager")

      #create and place widgets for credential manager
      self.label = tk.Label(master, text=f"Welcome, {self.user}!")
      self.label.pack(pady=10)

      self.save_button = tk.Button(master, text="Save Credential", command= self.save_credential(user))
      self.save_button.pack(pady=10)

      self.get_button = tk.Button(master, text="Get Credential",command = self.get_crdential)
      self.get_button.pack(pady=10)



   def save_credential(self,user):
      
