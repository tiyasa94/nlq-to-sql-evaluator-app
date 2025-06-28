import sqlparse
import math
import pandas as pd

def extract_operators_operands(sql_query):
    """Extracts SQL operators and operands from the given query."""
    parsed = sqlparse.parse(sql_query)
    tokens = [token.value.upper() for stmt in parsed for token in stmt.tokens if not token.is_whitespace]

    sql_operators = {
        'SELECT', 'FROM', 'WHERE', 'JOIN', 'GROUP BY', 'ORDER BY', 'INSERT',
        'UPDATE', 'DELETE', 'HAVING', 'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN',
        'ON', 'DISTINCT', 'AS', 'LIMIT', 'OFFSET', 'CASE', 'WHEN', 'THEN',
        'ELSE', 'END', 'AND', 'OR', 'NOT', 'LIKE', 'IN', 'BETWEEN',
        'EXISTS', 'OVER', 'ROW_NUMBER', 'RANK', 'DENSE_RANK', 'SUM', 'AVG',
        'UNION', 'ALL', 'INTERSECT', 'EXCEPT', 'ALTER'
    }

    operators = [token for token in tokens if token in sql_operators]
    operands = [token for token in tokens if token not in sql_operators and not token.isnumeric()]

    return set(operators), set(operands), operators, operands

def compute_halstead_metrics(sql_query):
    """Computes Halstead metrics for the given SQL query."""

    unique_operators, unique_operands, total_operators, total_operands = extract_operators_operands(sql_query)

    n1 = len(unique_operators)  # Unique operators
    n2 = len(unique_operands)   # Unique operands
    N1 = len(total_operators)   # Total operator occurrences
    N2 = len(total_operands)    # Total operand occurrences

    # Calculate Halstead metrics
    n = n1 + n2                  # Vocabulary
    N = N1 + N2                  # Length
    V = N * math.log2(n) if n > 0 else 0  # Volume
    D = (n1 / 2) * (N2 / n2) if n2 > 0 else 0  # Difficulty
    E = D * V                    # Effort

    metrics = {
        "Vocabulary": n,
        "Length": N,
        "Volume": V,
        "Difficulty": D,
        "Effort": E,
        "Errors": V / 3000,  # Estimated errors
    }
    return metrics

def compute_and_store_halstead_metrics(df):
    """
    Computes Halstead metrics for each SQL query in the DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame containing SQL queries.

    Returns:
        pd.DataFrame: Updated DataFrame with Halstead metrics added row-wise.
        dict: Average Halstead metrics across all queries.
    """
    # Apply Halstead metric computation for each query and expand metrics into separate columns
    halstead_results = df['generated_sql'].apply(compute_halstead_metrics)
    halstead_df = pd.DataFrame(halstead_results.tolist())

    # Append the Halstead metrics to the DataFrame
    updated_df = pd.concat([df, halstead_df], axis=1)

    # Calculate average metrics
    avg_metrics = halstead_df.mean().to_dict()

    return updated_df, avg_metrics
