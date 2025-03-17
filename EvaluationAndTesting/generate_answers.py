import pandas as pd
import json
import time
import sys
import os
miniproject_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(miniproject_path)
from Processing.rag_pipeline import query_rag_pipeline

# Check if the CSV file already exists
csv_path = "EvaluationAndTesting/Testing_data/generated_answers.csv"
if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
else:
    with open("EvaluationAndTesting/Testing_data/golden_set.json") as f:
        data = json.load(f)
    df = pd.DataFrame(data)


def run_rag_on_dataset(df):
    """Run the RAG pipeline on all questions in the dataset with a delay after every 2 queries."""
    
    for i, row in df.iterrows():
        df.at[i, "generated_answer"] = query_rag_pipeline(row["question"])
        print(i)
        # Add delay after every 2 queries
        if (i + 1) % 2 == 0:
            print(i, "🔹 Sleeping for 1 seconds to avoid rate limit...")
            time.sleep(1)  # Adjust delay time if needed
        if i % 100 == 0:
            df.to_csv("EvaluationAndTesting/Testing_data/generated_answers.csv", index=False)

    return df

# Apply RAG pipeline with delay
df = run_rag_on_dataset(df)

df.to_csv("EvaluationAndTesting/Testing_data/generated_answers.csv", index=False)