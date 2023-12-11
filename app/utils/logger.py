from datetime import date, datetime, timedelta
import logging
import os

from config import conf


if not os.path.exists(conf.LOG_PATH):
    os.makedirs(conf.LOG_PATH)

logging.basicConfig(
    format='%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%I:%M:%S'
)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s: %(message)s",
    "%Y-%m-%d %H:%M:%S"
)

file_name = date.today()

if datetime.now().hour == 0:
    file_name -= timedelta(days=1)


log_file = os.path.join(conf.LOG_PATH, f'{file_name}.log')

file_handler = logging.FileHandler(log_file , encoding='utf-8')
file_handler.setFormatter(formatter)

log = logging.getLogger(__name__)
# Define the level of log based on the enviroment of development
if not conf.DEBUG:
    log.setLevel(logging.INFO)
else:
    log.setLevel(logging.DEBUG)

log.addHandler(file_handler)
