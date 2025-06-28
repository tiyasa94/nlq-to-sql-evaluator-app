import streamlit as st
from .progress_bars import (
    display_metric_with_custom_progress_bar,
    display_metric_with_benchmark_progress_bar,
    display_simple_progress_bar,
)



def display_metrics_by_type(metrics, metric_type):
    """
    Display structured metric sections in the correct order with expandable descriptions and progress bars.

    Parameters:
        metrics (dict): Dictionary containing metric values.
        metric_type (str): Type of metrics (e.g., "performance", "entity_evaluation", "sql_injection").
    """
    # Define thresholds per metric type
    metric_thresholds = {
        "performance": {
            "Execution Time (s)": (5.0, 30.0),
            "Peak Memory Used (MB)": (1000.0, 3000.0),
            "CPU Time Used (seconds)": (0.1, 10.0),
            "Disk I/O Read (MB)": (0.1, 10.0),
            "Disk I/O Write (MB)": (0.1, 10.0),
        },
        "entity_evaluation": {
            "Table Match Score": (0, 1),  
            "Column Match Score": (0, 1),
            "Condition Match Score": (0, 1),
            "Aggregations Match Score": (0, 1),
        },
        "halstead": {
            "Vocabulary": (2, 50),
            "Length": (3, 100),
            "Volume": (5, 300),
            "Difficulty": (1, 15),
            "Effort": (5, 3000),
            "Estimated Errors": (0.0, 0.5),
        },
        "retrieval_accuracy": {
            "Average Rows Precision": (0, 1),
            "Average Column Precision": (0, 1),
            "Average Rows Recall": (0, 1),
            "Average Column Recall": (0, 1),
        },
        "sql_equivalence": {
            "Average SQL Equivalence Score": (0, 1),
        }
    }

    # Benchmarks for Halstead metrics
    halstead_benchmarks = {
        "Vocabulary": 8,
        "Length": 25,
        "Volume": 70,
        "Difficulty": 5,
        "Effort": 1000,
        "Estimated Errors": 0.02
    }

    # Handle SQL Injection separately
    if metric_type == "sql_injection":
        st.markdown("## SQL Injection Detection")

        with st.expander("ℹ️ What is SQL Injection Detection?"):
            st.write(
                "SQL Injection detection analyzes SQL queries to identify potential vulnerabilities. "
                "It flags patterns that may indicate an SQL injection attack, such as UNION-based injections, "
                "DROP TABLE attacks, or boolean-based attacks."
            )

        if sum(metrics.values()) == 0:
            st.success("✅ No SQL Injection patterns detected. All queries are safe!")
            return

        # Find max occurrences to normalize progress bars
        max_occurrence = max(metrics.values()) if metrics else 1  # Avoid division by zero

        col1, col2 = st.columns(2)
        for i, (pattern, count) in enumerate(metrics.items()):
            with (col1 if i % 2 == 0 else col2):
                display_metric_with_custom_progress_bar(pattern, count, 0, max_occurrence)
        return  


    section_info = {
        "performance": (
            "Performance Metrics",
            "These metrics assess the efficiency of the system, including execution time, memory usage, and CPU utilization."
        ),
        "halstead": (
            "Halstead Complexity Metrics",
            '''Halstead Complexity Metrics analyze code complexity based on operators, operands, and program difficulty. 
                Higher Vocabulary (n, The total number of unique operators and operands) suggests a complex query structure with multiple joins, conditions, or nested subqueries. 
                Queires with bigger Length (N, Total occurrences of operators and operands) queries might indicate inefficient SQL with redundant operations. 
                A higher Volume (N * log2(n), measures query information density) means a more information-heavy SQL, which might be harder to debug.
                Queries with many unique operators and operands are harder to optimize (Difficulty (n1/2) * (N2/n2), measures how difficult it is to understand or modify the query). 
                If Effort (D * V, estimated cognitive effort needed to understand the query) is high, the SQL query might be too complex for easy maintenance.
                Complex queries (high Volume) are more prone to syntax errors and logic flaws (Estimated Errors, V / 3000, an approximation of how many errors might exist).'''
        ),
        "entity_evaluation": (
            "Entity Evaluation Metrics",
            '''Validates whether the entities (tables, columns, conditions, aggregations) referenced in the generated SQL 
            query match with the same of ground truth SQL query. LLM extracts tables, columns, conditions, and aggregation functions 
            from 'generated_sql' and 'golden_sql' and the calculates table, column, and condition match scores based on precision, recall, and F1-score.'''
        ),
        "retrieval_accuracy": (
            "Data Retrieval Accuracy Metrics",
            '''These metrics measure how accurately the system retrieves relevant rows and columns in response to a query.
             It evaluates Output of the two SQL Queries in Comma Seperated Values and calculates Precision and Recall for rows and columns'''
        ),
        "sql_equivalence": (
            "SQL Semantic Equivalence Metrics",
            '''These metrics evaluate whether the generated SQL queries produce the same results as the expected reference queries.
            LLMSQLEquivalence is a metric that can be used to evaluate the equivalence of response query with reference query. 
            The metric also needs database schema to be used when comparing queries, this is inputted in reference_contexts. This metric is a binary metric, with 1 indicating that the SQL queries are semantically equivalent and 0 indicating that the SQL queries are not semantically equivalent.'''
        )
    }

    # Display section title and description
    title, description = section_info.get(metric_type, ("Unknown Metrics", "No description available."))
    st.markdown(f"## {title}")
    with st.expander(f"ℹ️ What is {title}?"):
        st.write(description)

    # Display metrics in two columns
    col1, col2 = st.columns(2)

    for i, (metric, value) in enumerate(metrics.items()):
        if metric in metric_thresholds.get(metric_type, {}):
            lower, upper = metric_thresholds[metric_type][metric]

            # Performance metrics use a simple progress bar (no "mean" label, different color)
            if metric_type == "performance":
                with (col1 if i % 2 == 0 else col2):
                    display_simple_progress_bar(metric, value, lower, upper)

            else:
                # For non-performance (including Halstead, entity, retrieval, etc.)
                # - Use Halstead benchmark logic if this is a Halstead metric
                if metric_type == "halstead":
                    # If below the benchmark => green; else => red
                    benchmark = halstead_benchmarks.get(metric, 0.85)
                    color = "green" if value < benchmark else "red"
                else:
                    # Fallback for other metric types
                    benchmark = 0.85
                    color = "green" if value >= benchmark else "red"

                with (col1 if i % 2 == 0 else col2):
                    display_metric_with_benchmark_progress_bar(
                        metric, 
                        value, 
                        lower, 
                        upper, 
                        benchmark, 
                        color, 
                        width="80%"
                    )