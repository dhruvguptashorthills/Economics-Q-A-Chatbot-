import pandas as pd
import json
import time
import sys
import os
miniproject_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(miniproject_path)
from Processing.rag_pipeline import pipeline

class RAGProcessor:
    def __init__(self, qa_folder):
        self.qa_folder = qa_folder
        self.json_files = {
            "multilingual": os.path.join(qa_folder, "multilingual.json"),
            "wrong_vocab_grammar": os.path.join(qa_folder, "wrong_vocab_grammar.json"),
            "misleading_out_of_context": os.path.join(qa_folder, "misleading.json")
        }
        self.csv_files = {
            "multilingual": os.path.join(qa_folder, "generated_answers_multilingual.csv"),
            "wrong_vocab_grammar": os.path.join(qa_folder, "generated_answers_wrong_vocab_grammar.csv"),
            "misleading_out_of_context": os.path.join(qa_folder, "generated_answers_misleading.csv")
        }

    def load_or_create_dataframe(self, csv_path, json_path):
        """Load the dataframe from CSV if it exists, otherwise create it from JSON."""
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
        else:
            with open(json_path) as f:
                data = json.load(f)
            df = pd.DataFrame(data)
        return df

    def run_rag_on_dataset(self, df, csv_path):
        """Run the RAG pipeline on all questions in the dataset with a delay after every 2 queries."""
        for i, row in df.iterrows():
            df.at[i, "generated_answer"] = pipeline.query_rag_pipeline(row["question"] + " answer should be in english only")
            print(i)
            # Add delay after every 2 queries
            if (i + 1) % 2 == 0:
                print(i, "🔹 Sleeping for 1 seconds to avoid rate limit...")
                time.sleep(1)
            if i % 10 == 0:
                self.save_dataframe_to_csv(df, csv_path)
        return df

    def save_dataframe_to_csv(self, df, csv_path):
        """Save the dataframe to a CSV file."""
        df.to_csv(csv_path, index=False)

    def process(self):
        """Process each category."""
        for category in self.json_files:
            json_path = self.json_files[category]
            csv_path = self.csv_files[category]

            # Load or create the dataframe
            df = self.load_or_create_dataframe(csv_path, json_path)

            # Apply RAG pipeline with delay
            df = self.run_rag_on_dataset(df, csv_path)

            # Save the final dataframe to CSV
            self.save_dataframe_to_csv(df, csv_path)

# Define file paths
qa_folder = "EvaluationAndTesting/Testing_data"

# Create an instance of RAGProcessor and process the data
processor = RAGProcessor(qa_folder)
processor.process()
