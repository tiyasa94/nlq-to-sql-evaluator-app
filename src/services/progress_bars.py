import streamlit as st

def display_metric_with_custom_progress_bar(metric_name, value, lower_threshold, upper_threshold):
    """
    Display a progress bar for SQL injection metrics.

    Parameters:
        metric_name (str): Name of the SQL injection pattern.
        value (float): Count of occurrences.
        lower_threshold (float): Minimum expected occurrences.
        upper_threshold (float): Maximum expected occurrences.
    """
    scaled_value = (value / upper_threshold) * 100
    scaled_value = min(max(scaled_value, 0), 100)

    progress_bar_html = f"""
    <div style="margin-bottom: 10px; max-width: 400px;">
        <strong>{metric_name}: {value}</strong>
        <div style="position: relative; height: 10px; background: #e0e0e0; border-radius: 5px; width: 80%;">
            <div style="width: {scaled_value}%; height: 100%; background: #F44336; border-radius: 5px;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 12px; margin-top: 3px; width: 80%;">
            <span>{lower_threshold}</span>
            <span>{(lower_threshold + upper_threshold) / 2:.2f} (Mean)</span>
            <span>{upper_threshold}</span>
        </div>
    </div>
    """
    st.markdown(progress_bar_html, unsafe_allow_html=True)


def display_metric_with_benchmark_progress_bar(metric_name, value, lower_threshold, upper_threshold, benchmark, color, width="80%"):
    """
    Display a progress bar for metrics with a benchmark threshold.

    Parameters:
        metric_name (str): Name of the metric.
        value (float): Current value of the metric.
        lower_threshold (float): Lower threshold for the metric.
        upper_threshold (float): Upper threshold for the metric.
        benchmark (float): Benchmark threshold for coloring logic.
        color (str): Color category (green/red based on benchmark check).
        width (str): Width of the progress bar (default: 80%).
    """
    scaled_value = (value / upper_threshold) * 100
    scaled_value = min(max(scaled_value, 0), 100)

    progress_bar_html = f"""
    <div style="margin-bottom: 10px; max-width: 400px;">
        <strong>{metric_name}: {value:.2f}</strong>
        <div style="position: relative; height: 10px; background: #e0e0e0; border-radius: 5px; width: {width};">
            <div style="width: {scaled_value}%; height: 100%; background: {color}; border-radius: 5px;"></div>
        </div>
        <div style="display: flex; justify-content: space-between; font-size: 12px; margin-top: 3px; width: {width};">
            <span>{lower_threshold}</span>
            <span>{benchmark:.2f} </span>
            <span>{upper_threshold}</span>
        </div>
    </div>
    """
    st.markdown(progress_bar_html, unsafe_allow_html=True)

def display_simple_progress_bar(metric_name, value, lower_threshold, upper_threshold, width="80%"):
    """
    Display a simple, neutral progress bar for performance metrics.

    Parameters:
        metric_name (str): Name of the metric.
        value (float): Current value of the metric.
        lower_threshold (float): Lower threshold for the metric.
        upper_threshold (float): Upper threshold for the metric.
        width (str): Width of the progress bar (default: 80%).
    """
    # Scale value between 0% and 100%
    scaled_value = ((value - lower_threshold) / (upper_threshold - lower_threshold)) * 100
    scaled_value = min(max(scaled_value, 0), 100)

    # Use a distinct color (e.g., a light blue) for the performance bar fill
    progress_bar_html = f"""
    <div style="margin-bottom: 10px; max-width: 400px;">
        <strong>{metric_name}: {value:.2f}</strong>
        <div style="position: relative; height: 10px; background: #e0e0e0; border-radius: 5px; width: {width};">
            <div style="width: {scaled_value}%; height: 100%; background: #2196F3; border-radius: 5px;"></div>
        </div>
        <!-- Only show min and max, no 'mean' label -->
        <div style="display: flex; justify-content: space-between; font-size: 12px; margin-top: 3px; width: {width};">
            <span>{lower_threshold}</span>
            <span>{upper_threshold}</span>
        </div>
    </div>
    """
    st.markdown(progress_bar_html, unsafe_allow_html=True)
