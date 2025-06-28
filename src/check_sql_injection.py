import re
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

# Define SQL injection patterns
SQLI_PATTERNS = {
    # Inline or Line-End Comments — used to ignore rest of query
    "Inline Comments": r"(--|#)",

    # UNION SELECT — used to extract additional data
    "UNION-Based Injection": r"\bUNION\b\s+SELECT\b",

    # Tautology-based OR logic — typical in basic injections like `OR 1=1`
    "Tautology OR 1=1": r"\bOR\b\s+(?:'[^']*'|\d+)\s*=\s*(?:'[^']*'|\d+)",

    # Malformed or logic-based use of OR without comparison to columns
    "Suspicious OR without Column": r"\bOR\b\s+['\d]",

    # DROP statements — destructive and rare in SELECT queries
    "DROP Table/Database": r"\bDROP\b\s+(TABLE|DATABASE)\b",

    # INSERT INTO VALUES — rarely used in generated user-facing SELECTs
    "INSERT Injection": r"\bINSERT\b\s+INTO\b\s+\w+\s+\bVALUES\b",

    # UPDATE statements with WHERE clause — may imply manipulation
    "UPDATE Injection": r"\bUPDATE\b\s+\w+\s+\bSET\b\s+\w+\s*=\s*.+?\bWHERE\b",

    # DELETE with WHERE — possibly destructive intent
    "DELETE Injection": r"\bDELETE\b\s+FROM\b\s+\w+\s+\bWHERE\b",

    # Single quote followed by comment — classic bypass
    "Single Quote with Comment": r"'[^']*'\s*--",

    # OS-level command execution — for SQL Server attacks
    "XP_CMDSHELL Execution": r"\bEXEC\b\s+XP_CMDSHELL\b",

    # Sleep/benchmark — time-based injection detection
    "Time Delay Injection": r"\b(SLEEP|BENCHMARK)\s*\(",
}





# SQLI_PATTERNS = {
#     "Inline Comments": r"--|#",
#     "UNION-Based Injection": r"\bUNION\b.*?\bSELECT\b",
#     "OR-Based Injection": r"\bSELECT\b.*?\bFROM\b.*?\bWHERE\b.*?\bOR\b.*?=",
#     "DROP Table/Database Attack": r"\bDROP\b.*?\b(TABLE|DATABASE)\b",
#     "INSERT Injection": r"\bINSERT\b.*?\bINTO\b.*?\bVALUES\b",
#     "UPDATE Injection": r"\bUPDATE\b.*?\bSET\b.*?\bWHERE\b",
#     "DELETE Injection": r"\bDELETE\b.*?\bFROM\b.*?\bWHERE\b",
#     "Single Quote with Comment": r"'.*?--",
#     "OS Command Execution": r"\bEXEC\b.*?\bXP_CMDSHELL\b",
#     "OR 1=1 Attack": r"\bor\b\s*\d+\s*=\s*\d+",
# }

def check_sql_injection(query: str):
    """
    Checks for potential SQL injection patterns in the given query.

    Parameters:
        query (str): The SQL query to check.

    Returns:
        dict: A dictionary with detected patterns and their status.
    """
    detected_patterns = []
    for pattern_name, pattern in SQLI_PATTERNS.items():
        if re.search(pattern, query, re.IGNORECASE):
            detected_patterns.append(pattern_name)

    if detected_patterns:
        return {"Status": "Potential SQL Injection Detected", "Patterns": detected_patterns}
    return {"Status": "Safe Query", "Patterns": []}

def detect_sql_injection_and_store_metrics(df):
    """
    Detects SQL injection in each query and adds results to the DataFrame.

    Parameters:
        df (pd.DataFrame): The DataFrame containing SQL queries.

    Returns:
        pd.DataFrame: Updated DataFrame with SQL injection detection results.
        dict: Average metrics for SQL injection patterns.
    """
    # Apply SQL injection detection
    injection_results = df['generated_sql'].apply(lambda query: check_sql_injection(str(query)))

    # Expand the results into separate columns
    results_df = pd.json_normalize(injection_results)
    updated_df = pd.concat([df, results_df], axis=1)

    # Calculate pattern occurrence counts
    pattern_counts = (
        results_df['Patterns']
        .explode()  # Flatten the list of patterns
        .value_counts()
        .to_dict()
    )

    # Calculate average occurrence count (for display purposes)
    total_patterns_detected = sum(pattern_counts.values())
    avg_metrics = {pattern: count for pattern, count in pattern_counts.items()}

    # If no patterns detected, provide a default metric summary
    if not avg_metrics:
        avg_metrics = {pattern: 0 for pattern in SQLI_PATTERNS.keys()}

    return updated_df, avg_metrics
