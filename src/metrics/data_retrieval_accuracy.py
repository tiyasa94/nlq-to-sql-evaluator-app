from ragas.metrics import DataCompyScore
from ragas.dataset_schema import SingleTurnSample
import asyncio
import pandas as pd

async def computy_compy_scores(data1, data2):
    """
    Compute precision and recall for rows and columns asynchronously.
    """
    sample = SingleTurnSample(response=data1, reference=data2)

    # Run all async tasks in parallel
    scores = await asyncio.gather(
        DataCompyScore(mode="columns", metric="precision").single_turn_ascore(sample),
        DataCompyScore(mode="columns", metric="recall").single_turn_ascore(sample),
        DataCompyScore(mode="rows", metric="precision").single_turn_ascore(sample),
        DataCompyScore(mode="rows", metric="recall").single_turn_ascore(sample),
    )

    return {
        "column_precision": scores[0],
        "column_recall": scores[1],
        "rows_precision": scores[2],
        "rows_recall": scores[3]
    }

def compute_and_return_retrieval_accuracy(db_manager, generated_sql, golden_sql):
    """
    Compute retrieval accuracy (precision and recall) for generated and golden SQL queries.

    Returns:
        pd.DataFrame: Updated DataFrame with retrieval accuracy metrics.
        dict: Average retrieval accuracy scores.
    """
    rows_precision_list, column_precision_list = [], []
    rows_recall_list, column_recall_list = [], []

    async def process_queries():
        """
        Runs retrieval accuracy calculations asynchronously for all SQL pairs.
        """
        tasks = []
        for gen_sql, gold_sql in zip(generated_sql, golden_sql):
            try:
                # Execute queries
                data1 = db_manager.execute_query_with_results(gen_sql)
                data2 = db_manager.execute_query_with_results(gold_sql)

                # Convert results to text format for comparison
                gen_data = '\n'.join(str(x) for x in data1)
                gold_data = '\n'.join(str(x) for x in data2)

                # Store async task
                tasks.append(computy_compy_scores(gen_data, gold_data))
            except Exception as e:
                print(f"Error processing SQL queries: {e}")
                tasks.append(asyncio.sleep(0))  # Placeholder to maintain indexing

        # Run all tasks in parallel
        results = await asyncio.gather(*tasks)

        for result in results:
            if isinstance(result, dict):
                rows_precision_list.append(result['rows_precision'])
                column_precision_list.append(result['column_precision'])
                rows_recall_list.append(result['rows_recall'])
                column_recall_list.append(result['column_recall'])
            else:
                rows_precision_list.append(0)
                column_precision_list.append(0)
                rows_recall_list.append(0)
                column_recall_list.append(0)

    # Run async function
    asyncio.run(process_queries())

    # Convert lists to DataFrame
    data = pd.DataFrame({
        'rows_precision': rows_precision_list,
        'column_precision': column_precision_list,
        'rows_recall': rows_recall_list,
        'column_recall': column_recall_list
    })

    # Compute average retrieval accuracy metrics
    avg_metrics = {
        "Average Rows Precision": data['rows_precision'].mean() if not data.empty else 0,
        "Average Column Precision": data['column_precision'].mean() if not data.empty else 0,
        "Average Rows Recall": data['rows_recall'].mean() if not data.empty else 0,
        "Average Column Recall": data['column_recall'].mean() if not data.empty else 0,
    }

    return data, avg_metrics  # ✅ Returns DataFrame + Average Metrics









# from ragas.metrics import DataCompyScore
# from ragas.dataset_schema import SingleTurnSample
# import asyncio
# import pandas as pd

# async def computy_compy_scores(data1,data2):
    
#     sample = SingleTurnSample(response=data1, reference=data2)

#     scorer = DataCompyScore(mode="columns", metric="precision")
#     column_precision= await scorer.single_turn_ascore(sample)
#     scorer = DataCompyScore(mode="columns", metric="recall")
#     column_recall= await scorer.single_turn_ascore(sample)


#     scorer = DataCompyScore(mode="rows", metric="precision")
#     rows_precision= await scorer.single_turn_ascore(sample)
#     scorer = DataCompyScore(mode="rows", metric="recall")
#     rows_recall= await scorer.single_turn_ascore(sample)

#     resp={

#         "rows_precision":rows_precision,
#         "column_precision":column_precision,
#         "rows_recall":rows_recall,
#         "column_recall":column_recall
#     }
#     return resp

# def compute_and_return_retrieval_accuracy(db_manager,generated_sql,golden_sql):
#     rows_precison_list=[]
#     column_precision_list=[]
#     rows_recall_list=[]
#     column_recall_list=[]
#     for i in range(0,len(generated_sql)):
#         data1=db_manager.execute_query_with_results(generated_sql[i])
#         data2=db_manager.execute_query_with_results(golden_sql[i])
#         gen_data = '\n'.join(str(x) for x in data1)
#         gold_data = '\n'.join(str(x) for x in data2)
#         metrics=asyncio.run(computy_compy_scores(gen_data,gold_data))
#         rows_precison_list.append(metrics['rows_precision'])
#         column_precision_list.append(metrics['column_precision'])
#         rows_recall_list.append(metrics['rows_recall'])
#         column_recall_list.append(metrics['column_recall'])
#     data=pd.DataFrame()
#     data['rows_precision']=rows_precison_list
#     data['column_precision']=column_precision_list
#     data['rows_recall']=rows_recall_list
#     data['column_recall']=column_recall_list
#     return data
