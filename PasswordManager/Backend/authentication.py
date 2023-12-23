import hashlib #Module provides common interface to multiple secure hashing algorithms.
import os
import sqlite3
from Backend.logger import Logger
from Backend.database import Database

class Authentication:

    def __init__(self):
        self.logger = Logger()
        self.database = Database()


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
    
    def update_user(self,username,hash_password,salt):
        
        self.logger.log_debug(f"Updating data for user :{username}")
        update_query = f"UPDATE users SET hashed_password = '{hash_password}', salt = '{salt}' WHERE username = '{username}';"
        if not self.database.execute_query(update_query):
            self.logger.log_error(f"Error in executing query {update_query}")



    #Store the user account details sqlite DB
    def store_user(self,username, hashed_password,salt):
        
        insert_query = f"INSERT INTO users (username, hashed_password, salt) VALUES ('{username}', '{hashed_password}', '{salt}');"
        if not self.database.execute_query(insert_query):
            self.logger.log_error(f"Error in executing query {insert_query}")

    def retrieve_userInfo(self,username):

        select_query = f"SELECT hashed_password, salt FROM users WHERE username = '{username}';"
        if self.database.execute_query(select_query):
            #Fetch the result (one row ) from the query
            user_info = self.database.cursor.fetchone()
            return user_info
        else:
            self.logger.log_error(f"Error in executing query {select_query}")
            return None
