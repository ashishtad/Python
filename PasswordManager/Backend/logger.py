
import logging
import datetime
import os

LOG_DIRECTORY = './Log'

class Logger:
    def __init__(self):
        if not os.path.exists(LOG_DIRECTORY):
            os.makedirs(LOG_DIRECTORY)
        #Generate time stamp for the log file name
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
        log_file_name = f'{LOG_DIRECTORY}/password_manager_{timestamp}.log'

        logging.basicConfig(filename=log_file_name,level=logging.DEBUG)
    
    def log_info(self, message):
        logging.info(message)
    
    def log_error(self,message):
        logging.error(message)
    
    def log_debug(self, message):
        logging.debug(message)