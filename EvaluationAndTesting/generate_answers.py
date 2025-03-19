import pandas as pd
import json
import time
import sys
import os
miniproject_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(miniproject_path)
from Processing.rag_pipeline import pipeline

def load_or_create_dataframe(csv_path, json_path):
    """Load the dataframe from CSV if it exists, otherwise create it from JSON."""
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        with open(json_path) as f:
            data = json.load(f)
        df = pd.DataFrame(data)
    return df

def run_rag_on_dataset(df):
    """Run the RAG pipeline on all questions in the dataset with a delay after every 2 queries."""
    for i, row in df.iterrows():
        df.at[i, "generated_answer"] = pipeline.query_rag_pipeline(row["question"])
        print(i)
        # Add delay after every 2 queries
        if (i + 1) % 2 == 0:
            print(i, "🔹 Sleeping for 1 seconds to avoid rate limit...")
            time.sleep(1)  # Adjust delay time if needed
        if i % 100 == 0:
            save_dataframe_to_csv(df, csv_path)
    return df

def save_dataframe_to_csv(df, csv_path):
    """Save the dataframe to a CSV file."""
    df.to_csv(csv_path, index=False)

# Define file paths
csv_path = "EvaluationAndTesting/Testing_data/generated_answers.csv"
json_path = "EvaluationAndTesting/Testing_data/golden_set.json"

# Load or create the dataframe
df = load_or_create_dataframe(csv_path, json_path)

# Apply RAG pipeline with delay
df = run_rag_on_dataset(df)

# Save the final dataframe to CSV
save_dataframe_to_csv(df, csv_path)