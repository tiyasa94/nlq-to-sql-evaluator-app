import streamlit as st
from database.database_connector import DatabaseManager


db_manager = DatabaseManager("t2s_sample.db")

def setup_database():
    """
    Sets up and connects to the SQLite database.
    Returns a DatabaseManager instance if successful, else None.
    """
    try:
        conn = db_manager.connect()
        if conn is None:
            st.error("Database connection failed. Please check the database setup.")
        return db_manager
    except Exception as e:
        st.error(f"Error setting up the database: {e}")
        return None


def execute_query(db_manager, sql_query):
    try:
        if db_manager:
            print("monitor_query_utilization is running...")
            results, metrics = monitor_query_utilization(lambda: db_manager.execute_query_with_results(sql_query))
            return results, metrics
        else:
            st.error("No database connection established.")
            return None, None
    except Exception as e:
        st.error(f"Error executing SQL query: {e}")
        return None, None

def cleanup():
    if db_manager:
        db_manager.close_connection()

cleanup()