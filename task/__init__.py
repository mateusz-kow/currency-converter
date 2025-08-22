import os
import logging
from task.utils.config import PROJECT_PATH

LOG_PATH = os.path.join(PROJECT_PATH, "app.log")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')

file_handler = logging.FileHandler(LOG_PATH, mode='a')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
