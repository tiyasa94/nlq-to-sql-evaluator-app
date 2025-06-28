import sqlite3
import os
from concurrent.futures import ThreadPoolExecutor
from database.load_data import LOAD_DATA_QUERIES
from database.load_tables_views import TABLES_VIEWS

DB_NAME = "t2s_sample.db"

def delete_database(db_name: str):
    """
    Deletes the specified SQLite database file.

    Parameters:
        db_name (str): The name of the database file to be deleted.
    """
    # Check if the database file exists
    if os.path.exists(db_name):
        os.remove(db_name)  # Delete the database file
        print(f"Database '{db_name}' has been deleted.")
    else:
        print(f"Database '{db_name}' does not exist.")

def configure_db(db_name: str):
    """
    Checks if a SQLite database exists with the given name.
    If it does not exist or does not match, creates a new database.

    Parameters:
        db_name (str): The name of the database to check/create.
    """
    # Check if the database file exists
    if os.path.exists(db_name):
        delete_database(db_name)
        print("Old DB deleted. Creating a new one...")
    
    # Create a new database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    print(f"Database '{db_name}' created successfully and connected.")
    return conn

def commit_n_close_db(con):
    """
    Commits the current transaction and closes the database cursor.

    Parameters:
        cursor (sqlite3.Cursor): The cursor object associated with the database connection.

    Returns:
        None
    """
    try:
        # Commit the current transaction
        con.commit()  # Ensure that the connection is committed
        print("Transaction committed successfully.")
        
        # Close the cursor
        con.close()
        print(f"Cursor closed successfully.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

def execute_queries(queries: list, cur: sqlite3.Cursor):
    """
    Executes a list of SQL queries using the provided cursor. This can be used with any query

    Parameters:
        queries (list): A list of SQL query strings to be executed.
        cursor (sqlite3.Cursor): The cursor object associated with the database connection.

    Returns:
        None
    """
    for query in queries:
        try:
            cur.execute(query)
            print(f"Query Executed Successfully: {query}")
        except Exception as e:
            print(f"Error executing query: {query}\nError: {e}")



def insert_data(con: sqlite3.Connection, data_query_dict: dict):
    """
    Inserts data into the database based on the provided data_query_dict.

    Parameters:
        con (sqlite3.Connection): The SQLite database connection.
        data_query_dict (dict): A dictionary containing table names as keys and a list
                                of tuples representing the values to insert.

    Returns:
        None
    """
    for key in data_query_dict:
        table_name = key
        
        # Extract values and their length
        values = data_query_dict[key][0]  # Column names
        insert_values = data_query_dict[key][1]  # Data tuples
        
        # Generate placeholders dynamically based on the number of columns
        num_columns = len(values)
        placeholders = ', '.join(['?' for _ in range(num_columns)])
        
        # Construct the insert query
        insert_query = f"INSERT INTO {table_name} ({', '.join(values)}) VALUES ({placeholders})"
        
        # Execute the insertion
        con.executemany(insert_query, insert_values)


def setup_and_populate_sqllite_db(db_name: str, table_queries: list[str], insert_queries: list[str]):
    """
    Sets up a SQLite database by configuring it and executing a list of SQL queries.

    Parameters:
        db_name (str): The name of the SQLite database file to be created or opened.
        queries (list): A list of SQL query strings to be executed on the database.

    Returns:
        None
    """
    # Configure the database and get a cursor
    conn = configure_db(db_name)
    
    # Execute queries to create tables
    print("-"*60)
    print("\n -----------------Creating tables in DB------------------ \n")
    print("-"*60)
    execute_queries(table_queries, conn)
    print("="*60)

    # Insert data in the tables
    print("-"*60)
    print("\n -----------------Populating tables with data------------------ \n")
    print("-"*60)
    print()
    for i in insert_queries:
        insert_data(conn, i)
    
    # Commit changes and close the cursor
    commit_n_close_db(conn)


