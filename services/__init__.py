import os

from .database import Database
from .task_manager import TaskManager
from .logging import setup_logger


ENV = os.getenv("PROFILE", "dev")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logger = setup_logger(LOG_LEVEL)


credentials = {
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASS'),
    'host': os.environ.get('DB_HOST'),
    'port': os.environ.get('DB_PORT'),
    'db_name': os.environ.get('DB_NAME'),
}

logger.debug('Connecting to database')
try:
    database = Database(credentials)
except Exception as e:
    logger.error(e)
    raise
logger.debug('Connected to database')


task_manager = TaskManager(database)

