import sqlite3
from Backend.logger import Logger

PWD_MANAGER_DATABASE = './PasswordManagerDataBase/password_manager.db'

class Database:

    def __init__(self):
        self.logger = Logger()
        self.init_database()

    def init_database(self):
        #Initiate a connection to sqlite DB and an iterator to iterate over DB
        try:
            self.connection = sqlite3.connect(PWD_MANAGER_DATABASE)
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
            self.logger.log_error(f"Error in init Database: {e}")
    
    def close_database(self):
        try:
            self.connection.close()
        except sqlite3.Error as e:
            self.logger.error(f"Error in closing database connection: {e}")
    
    #Execute the query on database
    def execute_query( self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            self.logger.log_error(f"Error in executing query: {e}")
            return False