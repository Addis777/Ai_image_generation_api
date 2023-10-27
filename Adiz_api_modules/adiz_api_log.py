import logging
import datetime

class ApiLogger:
    def __init__(self, log_file):
        self.log_file = log_file

    def log_info(self, message):
        log_format = '%(asctime)s - %(levelname)s: %(message)s'
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format=log_format)
        with open(self.log_file, 'a') as log_file:
            log_file.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' - INFO: ' + message + '\n')

    def log_error(self, message):
        log_format = '%(asctime)s - %(levelname)s: %(message)s'
        logging.basicConfig(filename=self.log_file, level=logging.ERROR, format=log_format)
        with open(self.log_file, 'a') as log_file:
            log_file.write(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' - ERROR: ' + message + '\n')
