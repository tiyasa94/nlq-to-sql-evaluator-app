# Text-to-SQL Pipeline Evaluator

## Introduction
The **Text-to-SQL Pipeline Evaluator** is designed to assess the performance of Text-to-SQL models by evaluating the correctness of entity recognition and SQL query generation. It ensures that generated SQL queries align with the expected schema, column references, and conditions. This asset enables structured evaluation by incorporating custom metrics to analyze various components of the Text-to-SQL conversion process.

## Business Challenge
One of the primary challenges in evaluating Text-to-SQL pipelines is the substantial amount of time required for validation due to the absence of appropriate metrics. Currently, verifying the correctness of AI-generated SQL queries involves extensive manual review by domain experts, which is inefficient and labor-intensive. The lack of standardized evaluation methods makes it difficult to assess the accuracy and effectiveness of SQL query generation models. This evaluator addresses these issues by:
- **Reducing Manual Effort**: Automating the validation process to minimize time spent on SQL verification.
- **Establishing Structured Metrics**: Providing well-defined evaluation criteria to assess query correctness.
- **Enhancing Scalability**: Allowing large-scale evaluation of multiple queries efficiently.
- **Improving Query Optimization**: Identifying inefficient SQL queries that could impact database performance.

## Use Case Details
To streamline the evaluation process, we have developed a **Streamlit application** that enables users to quickly validate the results of their Text-to-SQL pipelines. Users can simply upload the results, and with a single click, view all relevant evaluation metrics. The application provides:
- **Automated Analysis**: Instant calculation of key metrics for SQL query validation.
- **User-Friendly Interface**: Simplified workflow for evaluating multiple queries at once.
- **Comprehensive Insights**: Visual representation of query accuracy, efficiency, and semantic correctness.
- **Scalability**: The ability to handle large datasets for extensive evaluation.

This tool significantly reduces the manual effort required for validation, making it easier for developers and analysts to fine-tune their Text-to-SQL models effectively.

As a future enhancement, we plan to integrate all these evaluation metrics as a plugin within **Watsonx.governance**. This will allow for seamless governance, monitoring, and validation of Text-to-SQL pipelines within enterprise AI workflows.

## Domain
This evaluator is applicable across various industries and is designed for anyone who wants to evaluate their SQL generation pipeline. It can be used in:

## Intended Users
The **Text-to-SQL Pipeline Evaluator** is designed for:
- **AI Engineers & Data Scientists**: To assess and improve the accuracy of Text-to-SQL models and to ensure SQL queries generated from natural language inputs retrieve the correct data.

## Features
The evaluator includes the following key features:
- **Automated Processing**: Eliminates the need for manual validation by automating SQL evaluation.
- **Scalability**: Can handle batch evaluations for large datasets.
- **User Interface**: A **Streamlit-based** interactive application for easy result visualization.
- **Integration Ready**: Future compatibility with **Watsonx.governance** for enhanced AI pipeline monitoring and compliance.

## Metrics Details
Below are the details of the evaluation metrics used:
- **Performance Metrics**
Assess the efficiency of the system, including execution time, memory usage, and CPU utilization.
- **Halstead Complexity Metrics**
Analyze code complexity based on operators, operands, and query structure, measuring effort and difficulty.
- **SQL Injection Detection**
Identifies potential vulnerabilities and unsafe patterns in generated SQL queries.
- **Entity Recognition Evaluation**
Validates whether the tables, columns, conditions, and aggregations in the generated SQL match those in the ground truth SQL.
- **Data Retrieval Accuracy**
Measures how accurately the system retrieves relevant rows and columns in response to a query.
- **SQL Semantic Equivalence Score**
Determines whether the generated SQL query produces the same results as the expected ground-truth SQL, requiring database schema input.


## Steps to Use the Repository
Follow these steps to use the **Text-to-SQL Pipeline Evaluator**:

### 1. Clone the Repository
```sh
git clone https://github.com/tiyasa94/nlq-to-sql-evaluator-app.git
```

### 2. Install Dependencies
```sh
pip install -r requirements.txt
```

### 3. Create a `.env` File
The evaluator requires certain API credentials for Watsonx. Create a `.env` file in the root directory and add the following environment variables:
```sh
WATSONX_URL=<your_watsonx_url>
WATSONX_APIKEY=<your_watsonx_api_key>
WATSONX_PROJECT_ID=<your_watsonx_project_id>
```

### 4. In case you want to create and test using SQLite database, follow the below steps
```sh
Add your table data for schema using the load .py files as you see in src/database/tables
Update your .db filename in src/database/config_and_populate_db.py
Make necessary changes in load_data.py and load_tables_views.py
Connect with your database using database_connector.py
```

### 5. Create the .db file or just place it in the main workspace 
```sh
Update your .db filename in main.py here > db_manager = DatabaseManager("t2s_sample.db")
```


### 6. Run the Streamlit Application
```sh
streamlit run src/main.py
```

### 7. Upload Your CSV File
- If your CSV file contains only **`generated_sql`**, you will get:
  - **Performance Metrics**
  - **Halstead Complexity Scores**
  - **SQL Injection Detection**
- If your CSV file contains **`generated_sql`** and **`golden_sql`**, you will get:
  - **Entity Recognition Accuracy**
  - **Data Retrieval Accuracy**
- If your CSV file contains **`generated_sql`**, **`golden_sql`**, and **`database_schema`**, you will get:
  - **SQL Semantic Equivalence Score**
- Example: folder "data" -> "generated_sql_queries (1).csv"

### 8. View Evaluation Metrics
- Once uploaded, the system will automatically process the SQL queries and display:
  - Performance metrics
  - Entity evaluation
  - SQL semantic equivalence
  - Data retrieval accuracy
  - Halstead complexity scores
  - SQL injection detection

### 9. Analyze Results and Improve Queries
- Use the displayed insights to refine your Text-to-SQL models.
- Identify inefficiencies and optimize SQL query generation.

