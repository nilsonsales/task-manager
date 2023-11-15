import logging
import streamlit as st

from datetime import datetime
from .database import Database


logger = logging.getLogger(__name__)


class TaskManager:
    def __init__(self, db_conn: Database):
        self.db_conn = db_conn
        self.username = ''

    def insert_task(self, data):
        logger.debug(f"Inserting task: {data['task_name']}")
        data['username'] = self.username
        self.db_conn.insert_data(data)
        logger.info("Task inserted successfully.")

    def update_task(self, task_id, new_data: dict):
        new_data['updated_at'] = datetime.now().astimezone()
        self.db_conn.update_data(task_id, new_data)


    def list_in_progress_tasks(self):
        query = f"SELECT * FROM task_manager.tasks WHERE is_completed = False AND username = '{self.username}'"
        results = self.db_conn.execute_select_query(query)
        return results

    def list_completed_tasks(self):
        query = f"SELECT * FROM task_manager.tasks WHERE is_completed = True AND username = '{self.username}'"
        results = self.db_conn.execute_select_query(query)
        return results

    def list_all_tasks(self):
        query = f"SELECT * FROM task_manager.tasks WHERE username = '{self.username}'"
        results = self.db_conn.execute_select_query(query)
        return results

    def get_task_by_id(self, task_id):
        query = f"SELECT * FROM task_manager.tasks WHERE id = {task_id} AND username = '{self.username}'"
        task = self.db_conn.execute_select_query(query)
        return task

    def authenticate_user(self, username, password):
        authenticated = self.db_conn.authenticate_user(username, password)
        if authenticated:
            self.username = username
        return authenticated

    def user_exists(self, username):
        query = f"SELECT * FROM task_manager.users WHERE username = '{username}'"
        user = self.db_conn.execute_select_query(query)
        if len(user) > 0:
            return True
        return False

