
import logging

from .database import Database


logger = logging.getLogger(__name__)


class TaskManager:
    def __init__(self, db_conn: Database):
        self.db_conn = db_conn

    def insert_task(self, task_name, task_description, due_date,
        priority, is_completed):
        logger.info(f"Inserting task: {task_name}")
        data = {
            'task_name': task_name,
            'task_description': task_description,
            'due_date': due_date,
            'priority': priority,
            'is_completed': is_completed
        }
        self.db_conn.insert_data(data)
        logger.info("Task inserted successfully.")

    def update_task(self, task_id, new_data, updated_at):
        # TODO: Implement this method
        pass

    def list_in_progress_tasks(self):
        query = "SELECT * FROM task_manager.tasks WHERE is_completed = False"
        results = self.db_conn.execute_select_query(query)
        return results

    def list_completed_tasks(self):
        query = "SELECT * FROM task_manager.tasks WHERE is_completed = True"
        results = self.db_conn.execute_select_query(query)
        return results

    def list_all_tasks(self):
        query = "SELECT * FROM task_manager.tasks"
        results = self.db_conn.execute_select_query(query)
        return results
