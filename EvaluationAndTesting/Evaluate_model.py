import pandas as pd
from sentence_transformers import SentenceTransformer, util

class ModelEvaluator:
    def load_data(self, filepath):
        return pd.read_csv(filepath)

    def initialize_model(self, model_name):
        return SentenceTransformer(model_name)

    def semantic_similarity(self, model, pred, truth):
        emb1 = model.encode(pred, convert_to_tensor=True)
        emb2 = model.encode(truth, convert_to_tensor=True)
        return util.pytorch_cos_sim(emb1, emb2).item()

    def calculate_semantic_scores(self, df, model):
        df["Semantic_Similarity"] = df.apply(lambda row: self.semantic_similarity(model, row["generated_answer"], row["answer"]), axis=1)
        return df

    def calculate_statistics(self, df):
        semantic_score = df["Semantic_Similarity"].mean()
        num_cases_above_threshold = df[df["Semantic_Similarity"] > 0.5].shape[0]
        percentage_above_threshold = (num_cases_above_threshold / len(df)) * 100
        return semantic_score, percentage_above_threshold

    def save_results(self, df, semantic_score, percentage_above_threshold, csv_filepath, txt_filepath):
        df.to_csv(csv_filepath, index=False)
        with open(txt_filepath, "w") as report_file:
            report_file.write(f"Mean Semantic Similarity Score: {semantic_score:.4f}\n")
            report_file.write(f"Percentage of test cases above threshold: {percentage_above_threshold:.2f}%")

    def evaluate(self, data_filepath, model_name, csv_output_filepath, txt_output_filepath):
        df = self.load_data(data_filepath)
        model = self.initialize_model(model_name)
        df = self.calculate_semantic_scores(df, model)
        semantic_score, percentage_above_threshold = self.calculate_statistics(df)
        
        print(f"Mean Semantic Similarity Score: {semantic_score:.4f}")
        print(f"Percentage of test cases above threshold: {percentage_above_threshold:.2f}%")
        
        self.save_results(df, semantic_score, percentage_above_threshold, csv_output_filepath, txt_output_filepath)

def main():
    data_filepath = "EvaluationAndTesting/Testing_data/generated_answers.csv"
    csv_output_filepath = "EvaluationAndTesting/Evaluation/EvaluationReport.csv"
    txt_output_filepath = "EvaluationAndTesting/Evaluation/CummulativeEvaluationReport.txt"
    model_name = 'all-MiniLM-L6-v2'

    evaluator = ModelEvaluator()
    evaluator.evaluate(data_filepath, model_name, csv_output_filepath, txt_output_filepath)

if __name__ == "__main__":
    main()