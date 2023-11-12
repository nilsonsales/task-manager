import streamlit as st

from .database import Database
from .task_manager import TaskManager
from .logging import setup_logger


# Setup the app title
st.set_page_config(page_title='Simple Task Manager')

# Setup logger
logger = setup_logger()

# Connect to the database
logger.debug('Connecting to database')
try:
    credentials = {
        'username': st.secrets['database'].get('username'),
        'password': st.secrets['database'].get('password'),
        'host': st.secrets['database'].get('host'),
        'port': st.secrets['database'].get('port'),
        'database': st.secrets['database'].get('database'),
        'dialect': st.secrets['database'].get('dialect')
    }
    db_conn = Database(credentials)
except Exception as e:
    logger.error(e)
    raise
logger.debug('Connected to database')


task_manager = TaskManager(db_conn)

