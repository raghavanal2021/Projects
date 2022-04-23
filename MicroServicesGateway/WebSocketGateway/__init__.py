'''
Initialize Logging for the module.
'''
import json, logging
from concurrent_log_handler import ConcurrentRotatingFileHandler

'''
Get the logger for the class
'''
def getLogger(mod_name):
    logger = logging.getLogger(mod_name)
    file_name = f"{mod_name}.log"
    file_handler = ConcurrentRotatingFileHandler("./logs/SocketGateway.log",backupCount=2)
    file_formatter = logging.Formatter(json.dumps({'time':'%(asctime)s', 'name':'%(name)s','level':'%(levelname)s','message':'%(message)s'}))
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger