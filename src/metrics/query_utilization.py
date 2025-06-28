import psutil
import time
import pandas as pd
from memory_profiler import memory_usage

def monitor_query_utilization(query_execution_function, *args, **kwargs):
    """
    Monitor and measure system resources during query execution.

    Parameters:
        query_execution_function (function): The function to execute the query.

    Returns:
        tuple: (Query results, resource utilization metrics)
    """
    process = psutil.Process()

    # Capture initial state
    start_time = time.time()
    cpu_times_before = process.cpu_times()
    disk_io_before = psutil.disk_io_counters()

    try:
        # Measure peak memory usage during query execution
        peak_memory = memory_usage(
            (query_execution_function, args, kwargs), interval=0.1, retval=False
        )
        results = query_execution_function(*args, **kwargs)
    except Exception as e:
        raise RuntimeError(f"Error fetching query results: {e}")

    # Capture state after execution
    end_time = time.time()
    cpu_times_after = process.cpu_times()
    disk_io_after = psutil.disk_io_counters()

    # Calculate metrics
    execution_time = end_time - start_time
    cpu_used = (cpu_times_after.user - cpu_times_before.user) + \
               (cpu_times_after.system - cpu_times_before.system)
    peak_memory_used = max(peak_memory) if peak_memory else 0
    read_bytes = disk_io_after.read_bytes - disk_io_before.read_bytes
    write_bytes = disk_io_after.write_bytes - disk_io_before.write_bytes

    # Convert disk I/O to MB
    metrics = {
        "Execution Time (s)": float(execution_time),
        "Peak Memory Used (MB)": float(peak_memory_used),
        "CPU Time Used (seconds)": float(cpu_used),
        "Disk I/O Read (MB)": read_bytes / (1024 * 1024),
        "Disk I/O Write (MB)": write_bytes / (1024 * 1024),
    }

    return results, metrics


def calculate_and_store_metrics(df, db_manager):
    """
    Execute SQL queries, store metrics in the DataFrame, and return average metrics.

    Parameters:
        df (pd.DataFrame): The DataFrame containing SQL queries.
        db_manager (DatabaseManager): The database manager to execute SQL queries.

    Returns:
        tuple: (Updated DataFrame, dictionary of average metrics)
    """
    # Define columns for the new metrics
    metric_columns = [
        "Execution Time (s)", 
        "Peak Memory Used (MB)", 
        "CPU Time Used (seconds)", 
        "Disk I/O Read (MB)", 
        "Disk I/O Write (MB)"
    ]

    # Initialize columns with NaN values
    for column in metric_columns:
        df[column] = None

    for index, row in df.iterrows():
        generated_sql = row.get('generated_sql', '')
        if pd.notna(generated_sql) and generated_sql.strip():
            try:
                # Monitor performance during query execution
                _, metrics = monitor_query_utilization(lambda: db_manager.execute_query_with_results(generated_sql))

                # Add metrics to the corresponding row
                for metric, value in metrics.items():
                    df.at[index, metric] = value

            except Exception as e:
                df.at[index, 'Error'] = str(e)

    # Calculate average values for each metric
    avg_metrics = df[metric_columns].mean().to_dict()

    return df, avg_metrics
