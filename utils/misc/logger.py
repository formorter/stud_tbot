import logging
import sys
from logging.handlers import RotatingFileHandler
from time import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)
log_format = logging.Formatter('%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s')

file_handler = RotatingFileHandler(filename=f'./data/log/log.txt', mode='a', maxBytes=500*1024*1024, backupCount=1,encoding='utf-8')
file_handler.setFormatter(log_format)
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

if '-v' in sys.argv:
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(log_format)
    stream_handler.setLevel(logging.INFO)
    logger.addHandler(stream_handler)
