# Import necessary libraries and modules
import streamlit as st
import pandas as pd
import os
import base64
import asyncio
import warnings

# Import database and metric utility modules
from database.database_connector import DatabaseManager
from database.config_and_populate_db import *
from metrics.query_utilization import monitor_query_utilization, calculate_and_store_metrics
from metrics.halstead_scores import compute_halstead_metrics, compute_and_store_halstead_metrics
from metrics.check_sql_injection import detect_sql_injection_and_store_metrics
from metrics.data_retrieval_accuracy import compute_and_return_retrieval_accuracy
from metrics.sql_semantic_equivalence import WxAI_LLM
from metrics.entity_recognition import evaluate_entities_from_sql
from metrics.consistency_score import evaluate_queries_consistency
from metrics.validate_syntax import validate_syntax_and_store_metrics

# Import UI and service helpers
from services.background import add_bg_from_local, add_footer, set_custom_title, set_custom_subtitle
from services.database_service import setup_database, execute_query, cleanup
from services.display_metrics import display_metrics_by_type
from services.progress_bars import (
    display_metric_with_custom_progress_bar,
    display_metric_with_benchmark_progress_bar,
    display_simple_progress_bar
)
from services.evaluate_services import (
    evaluate_equivalence_metrics,
    evaluate_for_col_generate_sql,
    evaluate_for_col_generate_sql_golden_sql,
    evaluate_for_col_generate_sql_golden_sql_db_schema
)

# Suppress warnings globally for a cleaner UI
warnings.filterwarnings("ignore")

# Set up Streamlit page configuration
st.set_page_config(page_title="Text-to-SQL Pipeline Evaluator", layout="wide")


# Custom CSS for UI styling (buttons, radios, etc.)
custom_css = """
<style>
    div.stButton > button {
        color: white !important;
        background-color: #0049ff !important;
        font-weight: bold !important;
        font-size: 16px !important;
        border-radius: 8px;
        padding: 10px 20px;
    }
    div[data-baseweb="radio"] label {
        color: black !important;
        font-weight: bold;
        font-size: 12px;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# Add a custom footer to the app 
add_footer()

# Add a background image to the app
add_bg_from_local("image/bimage2.jpg")

# Display the main title in the center of the app
set_custom_title("Text-to-SQL Pipeline Evaluator", "#ffffff")

# Set up the database connection (returns a db_manager object)
db_manager = setup_database()

# Create three columns for layout; file uploader goes in the center column
col1, col2, col3 = st.columns([1, 1, 1])

# Place the file uploader widget in the center column
with col2:
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])


# Show CSV requirements/instructions in the center column
with col2:
    st.info('''
        Your CSV file should contain the following columns:

        - **`generated_sql`** (required): This column is necessary to evaluate performance and execution metrics.
        - **`golden_sql`** (optional but recommended): Needed to calculate ground-truth based metrics, 
          such as **Entity Recognition Score** and **Data Retrieval Accuracy**.
        - **`database_schema`** (optional): Required to compute **SQL Semantic Equivalence**.
    ''')

# If a file is uploaded, process it
if uploaded_file:
    uploaded_df = pd.read_csv(uploaded_file)

    # Check if the uploaded file is not empty
    if not uploaded_df.empty:
        try:
            # Check which columns are present in the uploaded CSV
            has_generated_sql = 'generated_sql' in uploaded_df.columns
            has_golden_sql = 'golden_sql' in uploaded_df.columns
            has_database_schema = 'database_schema' in uploaded_df.columns

            # Only 'generated_sql' column present
            if has_generated_sql and not has_golden_sql and not has_database_schema:
                st.write("Your CSV file contains only 'generated_sql' columns.")
                st.info("Hold tight while the metrics are being calculated...")
                evaluate_for_col_generate_sql(uploaded_df)

            # Both 'generated_sql' and 'golden_sql' columns present
            if has_generated_sql and has_golden_sql and not has_database_schema:
                st.write("Your CSV file contains 'generated_sql' and 'golden_sql' columns.")
                st.info("Hold tight while the metrics are being calculated...")
                evaluate_for_col_generate_sql_golden_sql(uploaded_df)

            # All three columns present
            if has_generated_sql and has_golden_sql and has_database_schema:
                st.write("Your CSV file contains all 3 columns.")
                st.info("Hold tight while the metrics are being calculated...")
                evaluate_for_col_generate_sql_golden_sql_db_schema(uploaded_df)

        except Exception as e:
            # Display any error that occurs during metric evaluation
            st.error(f"Error in metrics evaluation: {e}")
    else:
        # Warn if the uploaded CSV is empty
        st.warning("The uploaded CSV file is empty. Please provide a valid file.")

# Clean up database connections or resources at the end
cleanup()

