import pandas as pd
import logging

from sqlalchemy import text, create_engine


logger = logging.getLogger(__name__)

class Database:
    def __init__(self, credentials):
        """
        Connect to the database
        """
        self.dialect = credentials['dialect']
        self.host = credentials['host']
        self.username = credentials['username']
        self.password = credentials['password']
        self.db_name = credentials['database']
        self.port = credentials['port']

        url = f"{self.dialect}://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"
        self.engine = create_engine(url)
        self.connection = self.engine.connect()

    def close(self):
        self.connection.close()

    def insert_data(self, params: dict):
        column_names = ', '.join(params.keys())
        values = ':'+', :'.join(params.keys())

        query = text(f"INSERT INTO task_manager.tasks ({column_names}) VALUES ({values})")
        logger.debug(f'Inserting data:\n{query}')

        self.connection.execute(query, parameters=params)
        self.connection.commit()

    def update_data(self, id, params: dict):
        columns_updates = ''.join([f'{key} = :{key}, ' for key in params.keys()])
        columns_updates = columns_updates[:-2]

        query = text(f"UPDATE task_manager.tasks SET {columns_updates} WHERE id = {id}")
        logger.debug(f'Updating data:\n{query}')

        self.connection.execute(query, parameters=params)
        self.connection.commit()

    def execute_select_query(self, query: str):
        query = text(query)

        logger.debug(f'Executing query:\n{query}')
        # Load the query results into a pandas DataFrame
        df = pd.read_sql_query(query, self.connection)
        return df

    def add_user(self, username, password):
        # Insert the user into the 'users' table
        query = text(f"INSERT INTO task_manager.users (username, password) VALUES ('{username}', crypt('{password}', gen_salt('bf')))")

        self.connection.execute(query)
        self.connection.commit()





