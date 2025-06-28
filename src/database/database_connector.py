import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name: str):
        """
        Initializes the DatabaseManager with the specified database name.

        Parameters:
            db_name (str): The name of the SQLite database file.
        """
        self.db_name = db_name
        self.conn = None

    def connect(self):
        """
        Establishes a connection to the SQLite database.

        Returns:
            sqlite3.Connection: The connection object.
        """
        try:
            self.conn = sqlite3.connect(self.db_name)
            print(f"Connected to database '{self.db_name}'.")
            return self.conn
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def close_connection(self):
        """
        Closes the connection to the SQLite database.
        """
        if self.conn:
            try:
                self.conn.close()
                print(f"Connection to '{self.db_name}' closed.")
            except sqlite3.Error as e:
                print(f"Error closing the connection: {e}")

    def execute_query(self, query: str):
        """
        Executes a single SQL query on the database.

        Parameters:
            query (str): The SQL query to execute.

        Returns:
            None
        """
        try:
            if not self.conn:
                raise Exception("No database connection established.")
            
            cursor = self.conn.cursor()
            cursor.execute(query)
            self.conn.commit()
            print(f"Query executed successfully:\n{query}")
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")

    def execute_query_with_results(self, query: str):
        """
        Executes a query and fetches results from the database.

        Parameters:
            query (str): The SQL query to execute.

        Returns:
            list: The query results.
        """
        try:
            if not self.conn:
                raise Exception("No database connection established.")
            
            cursor = self.conn.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Error fetching query results: {e}")
            return []
