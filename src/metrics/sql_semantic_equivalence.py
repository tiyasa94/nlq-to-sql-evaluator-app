import os
import json
import pandas as pd
from dotenv import load_dotenv
from langchain_ibm import WatsonxLLM

# Load environment variables
load_dotenv()

# Watsonx Configuration
IBM_CLOUD_URL = os.getenv("WATSONX_URL")
IBM_CLOUD_API_KEY = os.getenv("WATSONX_APIKEY")
WML_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

class WxAI_LLM:
    def __init__(self):
        """
        Initializes the Watsonx LLM configuration.
        """
        self.watsonx_url = IBM_CLOUD_URL
        self.watsonx_api = IBM_CLOUD_API_KEY
        self.watsonx_project_id = WML_PROJECT_ID

        if not all([self.watsonx_url, self.watsonx_api, self.watsonx_project_id]):
            raise ValueError("❌ Watsonx environment variables are missing. Please check .env file.")

        self.parameters = {
            "decoding_method": "sample",
            "max_new_tokens": 500,
            "temperature": 0.8,
            "top_p": 0.7,
            "stop_sequences": ["}"]
        }

        self.watsonx_llm = WatsonxLLM(
            model_id="mistralai/mixtral-8x7b-instruct-v01",
            url=self.watsonx_url,
            apikey=self.watsonx_api,
            project_id=self.watsonx_project_id,
            params=self.parameters,
        )

    def compute_sql_semantic_equivalence_score(self, reference: str, response_input: str, database_schema: str):
        """
        Computes SQL Semantic Equivalence Score between two queries.

        Parameters:
            reference (str): The reference SQL query (golden standard).
            response_input (str): The generated SQL query.
            database_schema (str): The database schema to validate.

        Returns:
            int: 1 if queries are equivalent, 0 otherwise.
        """
        prompt = f"""
        Compare two SQL queries (Q1 and Q2) based on the provided database schema. Explain both queries, 
        determine if they are logically equivalent, and return only the JSON response.

        Example:
        Input:
            reference="SELECT id, name FROM users WHERE active = 1;",
            response="SELECT id, name FROM users WHERE active = true;",
            database_schema=\"""
                Table users:
                - id: INT
                - name: VARCHAR
                - active: BOOLEAN
            \""",

        Output:
        {{
            "equivalence": true
        }}

        SQL Query:
        reference={reference}
        response={response_input}
        database_schema={database_schema}

        Response:
        """

        try:
            response = self.watsonx_llm.generate([prompt])
            response_text = response.generations[0][0].text.strip()

            result = json.loads(response_text)
            return 1 if result.get("equivalence", False) else 0

        except json.JSONDecodeError:
            return 0  # Default to not equivalent if parsing fails
        except Exception as e:
            print(f"Error in WatsonxLLM: {e}")
            return 0

    def evaluate_equivalence_from_csv(self, df: pd.DataFrame):
        """
        Computes the average SQL semantic equivalence score for all queries in a DataFrame.

        Parameters:
            df (pd.DataFrame): DataFrame containing 'generated_sql', 'golden_sql', and 'database_schema'.

        Returns:
            dict: Dictionary containing the average equivalence score.
        """
        equivalence_scores = []

        for _, row in df.iterrows():
            score = self.compute_sql_semantic_equivalence_score(
                row["golden_sql"], row["generated_sql"], row.get("database_schema", "")
            )
            equivalence_scores.append(score)

        avg_equivalence_score = sum(equivalence_scores) / len(equivalence_scores) if equivalence_scores else 0

        return {"Average SQL Equivalence Score": avg_equivalence_score}
