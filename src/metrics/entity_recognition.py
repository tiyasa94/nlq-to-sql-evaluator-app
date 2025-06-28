import pandas as pd
import json
import os
from langchain_ibm import WatsonxLLM
from dotenv import load_dotenv
import warnings

warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()

# Watsonx configuration
WATSONX_URL = os.getenv("WATSONX_URL")
WATSONX_APIKEY = os.getenv("WATSONX_APIKEY")
WML_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

def calculate_mean(values):
    return sum(values) / len(values) if values else 0





def evaluate_entities_from_sql(df):
    """
    Evaluate the correctness of table, columns, and conditions for each row in a DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame containing 'reference_output' and 'generated_text'.

    Returns:
        pd.DataFrame: Updated DataFrame with evaluation metrics added.
    """

    # Initialize the WxAI Agent
    class WxAI_Agent:
        def __init__(self):
            # Watsonx LLM configuration
            self.watsonx_url = WATSONX_URL
            self.watsonx_api = WATSONX_APIKEY
            self.watsonx_project_id = WML_PROJECT_ID


            if not self.watsonx_url or not self.watsonx_api or not self.watsonx_project_id:
                raise ValueError("Watsonx environment variables are not set.")

            self.parameters = {
                "decoding_method": "greedy",
                "max_new_tokens": 250,
                # "temperature": 0.8,
                # "top_p": 0.7,
                "stop_sequences": ["}"]
            }

            self.watsonx_llm = WatsonxLLM(
                model_id="mistralai/mixtral-8x7b-instruct-v01",
                url=self.watsonx_url,
                apikey=self.watsonx_api,
                project_id=self.watsonx_project_id,
                params=self.parameters,
            )

        def extract_entities_from_sql(self, sql_query):
            """
            Use WatsonxLLM to extract entities (tables, columns, and conditions) from an SQL query.

            Parameters:
                sql_query (str): The SQL query to analyze.

            Returns:
                dict: Extracted entities in JSON format.
            """
            # Construct the prompt
            prompt = f"""
            You are a highly skilled AI model specializing in SQL analysis. Your task is to extract entities from SQL queries. 
            For the given SQL query, identify the table names, column names, conditions, and aggregate functions used. 
            If there is no entity recognized, you have to put "NA" there.
            Do not give anything other than the JSON below.
            
            Examples for you:
            Example1: 
            SQL Query: SELECT partner_org_name, SUM(open_pipeline_amount) AS total_pipeline FROM account_partner_table WHERE open_pipeline_amount IS NOT NULL GROUP BY partner_org_name ORDER BY total_pipeline DESC LIMIT 1;
            {{
                "tables": ["account_partner_table"],
                "columns": ["partner_org_name", "open_pipeline_amount"],
                "conditions": ["open_pipeline_amount IS NOT NULL"],
                "aggregate_functions": ["SUM(open_pipeline_amount)"]
            }}
            
            Example2: 
            SQL Query: SELECT account_name FROM account_product_table JOIN account_quality_table ON customer_to_product = 'ServiceCloud' WHERE propensity > 80;
            {{
                "tables": ["account_product_table", "account_quality_table"],
                "columns": ["account_name", "customer_to_product", "propensity"],
                "conditions": ["customer_to_product = 'ServiceCloud'", "propensity > 80"],
                "aggregate_functions": ["NA"]
            }}

            Example3:
            SQL Query: SELECT first_name FROM employees;
            {{
                "tables": ["employees"],
                "columns": ["first_name"],
                "conditions": ["NA"],
                "aggregate_functions": ["NA"]
            }}
                        
            Provide the response in the following JSON format:
            {{
                "tables": [<list of table names>],
                "columns": [<list of column names>],
                "conditions": [<list of conditions>],
                "aggregate_functions": [<list of aggregate functions>]
            }}
                        
            SQL Query:
            {sql_query}
            
            Response:
            """

            response = self.watsonx_llm.generate([prompt])
            response_text = response.generations[0][0].text.strip()
            return json.loads(response_text)

    # Initialize the agent
    agent = WxAI_Agent()

    # Initialize lists to store evaluation metrics and extracted entities
    table_match_scores = []
    column_match_scores = []
    condition_match_scores = []
    af_match_scores = []

    generated_tables = []
    generated_columns = []
    generated_conditions = []
    generated_aggregate_functions = []

    golden_tables = []
    golden_columns = []
    golden_conditions = []
    golden_aggregate_functions = []

    # Process each row in the DataFrame
    for _, row in df.iterrows():
        print('row', row)
        # Extract entities for reference_output and generated_text
        golden_entities = agent.extract_entities_from_sql(row['golden_sql'])
        generated_entities = agent.extract_entities_from_sql(row['generated_sql'])

        # Store the extracted entities
        generated_tables.append(generated_entities.get("tables", []))
        generated_columns.append(generated_entities.get("columns", []))
        generated_conditions.append(generated_entities.get("conditions", []))
        generated_aggregate_functions.append(generated_entities.get("aggregate_functions", []))

        golden_tables.append(golden_entities.get("tables", []))
        golden_columns.append(golden_entities.get("columns", []))
        golden_conditions.append(golden_entities.get("conditions", []))
        golden_aggregate_functions.append(golden_entities.get("aggregate_functions", []))

        # Evaluate Tables
        table_match_scores.append(int(golden_entities.get("tables", []) == generated_entities.get("tables", [])))

        # Evaluate Columns
        ground_truth_columns = set(golden_entities.get("columns", []))
        generated_columns_set = set(generated_entities.get("columns", []))
        columns_precision = len(ground_truth_columns & generated_columns_set) / len(generated_columns_set) if generated_columns_set else 0
        columns_recall = len(ground_truth_columns & generated_columns_set) / len(ground_truth_columns) if ground_truth_columns else 0
        column_match_scores.append(
            2 * (columns_precision * columns_recall) / (columns_precision + columns_recall)
            if columns_precision + columns_recall > 0
            else 0
        )

        # Evaluate Conditions
        ground_truth_conditions = set(golden_entities.get("conditions", []))
        generated_conditions_set = set(generated_entities.get("conditions", []))
        conditions_precision = len(ground_truth_conditions & generated_conditions_set) / len(generated_conditions_set) if generated_conditions_set else 0
        conditions_recall = len(ground_truth_conditions & generated_conditions_set) / len(ground_truth_conditions) if ground_truth_conditions else 0
        condition_match_scores.append(
            2 * (conditions_precision * conditions_recall) / (conditions_precision + conditions_recall)
            if conditions_precision + conditions_recall > 0
            else 0
        )

        # Evaluate Aggregate Functions
        ground_truth_af = set(golden_entities.get("aggregate_functions", []))
        generated_af = set(generated_entities.get("aggregate_functions", []))
        af_precision = len(ground_truth_af & generated_af) / len(generated_af) if generated_af else 0
        af_recall = len(ground_truth_af & generated_af) / len(ground_truth_af) if ground_truth_af else 0
        af_match_scores.append(
            2 * (af_precision * af_recall) / (af_precision + af_recall)
            if af_precision + af_recall > 0
            else 0
        )

    # Add the extracted entities and evaluation metrics back to the DataFrame
    df['Generated Tables'] = generated_tables
    df['Generated Columns'] = generated_columns
    df['Generated Conditions'] = generated_conditions
    df['Generated Aggregate Functions'] = generated_aggregate_functions

    df['Golden Tables'] = golden_tables
    df['Golden Columns'] = golden_columns
    df['Golden Conditions'] = golden_conditions
    df['Golden Aggregate Functions'] = golden_aggregate_functions

    df['Table Match Score'] = table_match_scores
    df['Column Match Score'] = column_match_scores
    df['Condition Match Score'] = condition_match_scores
    df['Aggregations Match Score'] = af_match_scores


    avg_metrics = {
        "Table Match Score": calculate_mean(table_match_scores),
        "Column Match Score": calculate_mean(column_match_scores),
        "Condition Match Score": calculate_mean(condition_match_scores),
        "Aggregations Match Score": calculate_mean(af_match_scores)
    }

    return df, avg_metrics