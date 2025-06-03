import os
# import sys
import logging
from task.utils.config import PROJECT_PATH

LOG_PATH = os.path.join(PROJECT_PATH, "app.log")

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(message)s')

file_handler = logging.FileHandler(LOG_PATH, mode='w')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# stdout_handler = logging.StreamHandler(sys.stdout)
# stdout_handler.setLevel(logging.INFO)
# stdout_handler.addFilter(lambda record: record.levelno < logging.ERROR)
# stdout_handler.setFormatter(formatter)
# logger.addHandler(stdout_handler)

# stderr_handler = logging.StreamHandler(sys.stderr)
# stderr_handler.setLevel(logging.ERROR)
# stderr_handler.setFormatter(formatter)
# logger.addHandler(stderr_handler)
