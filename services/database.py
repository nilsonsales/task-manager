from sqlalchemy import create_engine, text
import pandas as pd
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, credentials):
        """
        Initializes a new instance of the class.
        Parameters:
            credentials (dict): A dictionary containing the credentials for the database connection.
                The dictionary must have the following keys:
                - host (str): The host name or IP address of the database server.
                - user (str): The username for the database connection.
                - password (str): The password for the database connection.
                - db_name (str): The name of the database to connect to.
                - port (int): The port number for the database connection.
        Returns:
            None
        """
        self.host = credentials['host']
        self.user = credentials['user']
        self.password = credentials['password']
        self.db_name = credentials['db_name']
        self.port = credentials['port']

        url = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"
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
        logger.info(f"Updating task: {id}")
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




