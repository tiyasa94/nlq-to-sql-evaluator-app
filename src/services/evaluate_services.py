import streamlit as st

from database.config_and_populate_db import *
from metrics.query_utilization import calculate_and_store_metrics
from metrics.halstead_scores import compute_and_store_halstead_metrics
from metrics.check_sql_injection import detect_sql_injection_and_store_metrics
from metrics.data_retrieval_accuracy import compute_and_return_retrieval_accuracy
from metrics.sql_semantic_equivalence import WxAI_LLM
from metrics.entity_recognition import evaluate_entities_from_sql
from services.display_metrics import display_metrics_by_type
import warnings
from services.database_service import setup_database


db_manager = setup_database()

def evaluate_equivalence_metrics(uploaded_df):
    """
    Evaluate SQL Semantic Equivalence for all queries in the uploaded DataFrame.

    Parameters:
        uploaded_df (pd.DataFrame): The DataFrame containing SQL queries.

    Returns:
        pd.DataFrame: Updated DataFrame with SQL equivalence scores.
    """
    # Step 1: Initialize Watsonx LLM Agent
    sql_equivalence_agent = WxAI_LLM()

    # Step 2: Compute SQL Equivalence Scores for all rows
    equivalence_metrics = sql_equivalence_agent.evaluate_equivalence_from_csv(uploaded_df)

    # Step 3: Display Equivalence Metrics with Progress Bar
    display_metrics_by_type(equivalence_metrics, metric_type="sql_equivalence")

    return uploaded_df



def evaluate_for_col_generate_sql(uploaded_df):

    # Display SQL Injection metrics (now with progress bars)
    print("SQL injection is runnning...")
    updated_df, sql_injection_summary = detect_sql_injection_and_store_metrics(uploaded_df)
    display_metrics_by_type(sql_injection_summary, metric_type="sql_injection")

    # Compute and display Halstead Complexity Metrics
    print("Halstead complexity is running...")
    updated_df, avg_halstead_metrics = compute_and_store_halstead_metrics(updated_df)
    display_metrics_by_type(avg_halstead_metrics, metric_type="halstead")

    # Execute queries and calculate performance metrics
    updated_df, avg_metrics = calculate_and_store_metrics(uploaded_df, db_manager)
    display_metrics_by_type(avg_metrics, metric_type="performance")    


def evaluate_for_col_generate_sql_golden_sql(uploaded_df):
    
    # Entity Recognition Evaluation
    updated_df, entity_metrics= evaluate_entities_from_sql(uploaded_df) 
    display_metrics_by_type(entity_metrics, metric_type="entity_evaluation")

    # Compute and display Halstead Complexity Metrics
    updated_df, avg_halstead_metrics = compute_and_store_halstead_metrics(updated_df)
    display_metrics_by_type(avg_halstead_metrics, metric_type="halstead")

     # Display SQL Injection metrics (now with progress bars)
    updated_df, sql_injection_summary = detect_sql_injection_and_store_metrics(updated_df)
    display_metrics_by_type(sql_injection_summary, metric_type="sql_injection")

    # Display data retrieval metric
    generated_sql = updated_df['generated_sql'].tolist()
    golden_sql = updated_df['golden_sql'].tolist()
    print("Retrieval Accuracy is running...")
    updated_df, avg_retrieval_accuracy = compute_and_return_retrieval_accuracy(db_manager, generated_sql, golden_sql)
    display_metrics_by_type(avg_retrieval_accuracy, metric_type="retrieval_accuracy")

    # Execute queries and calculate performance metrics
    updated_df, avg_metrics = calculate_and_store_metrics(uploaded_df, db_manager)
    display_metrics_by_type(avg_metrics, metric_type="performance")



def evaluate_for_col_generate_sql_golden_sql_db_schema(uploaded_df):
    
    # Entity Recognition Evaluation
    updated_df, entity_metrics= evaluate_entities_from_sql(uploaded_df) 
    display_metrics_by_type(entity_metrics, metric_type="entity_evaluation")

    # Compute and display Halstead Complexity Metrics
    updated_df, avg_halstead_metrics = compute_and_store_halstead_metrics(updated_df)
    display_metrics_by_type(avg_halstead_metrics, metric_type="halstead")

    # sql equivalance score
    evaluate_equivalence_metrics(uploaded_df)

     # Display SQL Injection metrics (now with progress bars)
    updated_df, sql_injection_summary = detect_sql_injection_and_store_metrics(updated_df)
    display_metrics_by_type(sql_injection_summary, metric_type="sql_injection")

    # Display data retrieval metric
    generated_sql = updated_df['generated_sql'].tolist()
    golden_sql = updated_df['golden_sql'].tolist()
    updated_df, avg_retrieval_accuracy = compute_and_return_retrieval_accuracy(db_manager, generated_sql, golden_sql)
    display_metrics_by_type(avg_retrieval_accuracy, metric_type="retrieval_accuracy")

    # Execute queries and calculate performance metrics
    updated_df, avg_metrics = calculate_and_store_metrics(uploaded_df, db_manager)
    display_metrics_by_type(avg_metrics, metric_type="performance")