import pandas as pd
from sentence_transformers import SentenceTransformer, util
from rouge import Rouge
from nltk.translate.bleu_score import sentence_bleu
from bert_score import score as bert_score

class ModelEvaluator:
    def load_data(self, filepaths):
        dfs = [pd.read_csv(filepath) for filepath in filepaths]
        return pd.concat(dfs, ignore_index=True)

    def initialize_model(self, model_name):
        return SentenceTransformer(model_name)

    def semantic_similarity(self, model, text1, text2):
        if pd.isna(text1) or pd.isna(text2):
            return 0.0
        emb1 = model.encode(text1, convert_to_tensor=True)
        emb2 = model.encode(text2, convert_to_tensor=True)
        return util.pytorch_cos_sim(emb1, emb2).item()

    def calculate_rouge(self, df):
        rouge = Rouge()
        return df.apply(lambda row: rouge.get_scores(row["generated_answer"], row["answer"])[0]['rouge-l']['f'], axis=1)

    def calculate_bleu(self, df):
        return df.apply(lambda row: sentence_bleu([row["answer"].split()], row["generated_answer"].split()), axis=1)
    
    def calculate_bert_score(self, df):
        P, R, F1 = bert_score(df["generated_answer"].tolist(), df["answer"].tolist(), lang="en", rescale_with_baseline=True)
        return F1.tolist()

    def calculate_scores(self, df, model):
        df["Semantic Similarity"] = df.apply(lambda row: self.semantic_similarity(model, row["generated_answer"], row["answer"]), axis=1)
        df["Rouge"] = self.calculate_rouge(df)
        df["Bleu"] = self.calculate_bleu(df)
        df["BERTScore"] = self.calculate_bert_score(df)
        df["Final Score"] = df["Semantic Similarity"]
        df["Pass/Fail"] = self.assign_pass_fail(df)
        return df

    def assign_pass_fail(self, df):
        return df["Final Score"].apply(lambda x: "Pass" if x >= 0.5 else "Fail")

    def calculate_statistics(self, df):
        scores = {metric: df[metric].mean() for metric in ["Semantic Similarity", "Rouge", "Bleu", "BERTScore", "Final Score"]}
        total_cases = len(df)
        passed_cases = (df["Pass/Fail"] == "Pass").sum()
        failed_cases = (df["Pass/Fail"] == "Fail").sum()
        percentage_above_threshold = (passed_cases / total_cases) * 100 if total_cases > 0 else 0
        
        statistics = {
            "Mean Scores": scores,
            "Total Test Cases": total_cases,
            "Passed Test Cases": passed_cases,
            "Failed Test Cases": failed_cases,
            "Percentage Above Threshold": percentage_above_threshold
        }
        return statistics

    def save_results(self, df, statistics, excel_filepath, txt_filepath):
        df.to_excel(excel_filepath, index=False)
        with pd.ExcelWriter(excel_filepath, engine='openpyxl', mode='a') as writer:
            summary_df = pd.DataFrame({"Metric": list(statistics["Mean Scores"].keys()), "Score": list(statistics["Mean Scores"].values())})
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        with open(txt_filepath, "w") as txt_file:
            txt_file.write("Evaluation Summary:\n")
            for key, value in statistics.items():
                if isinstance(value, dict):
                    txt_file.write(f"{key}:\n")
                    for sub_key, sub_value in value.items():
                        txt_file.write(f"  {sub_key}: {sub_value:.4f}\n")
                else:
                    txt_file.write(f"{key}: {value}\n")
    
    def evaluate(self, data_filepaths, model_name, excel_output_filepath, txt_output_filepath):
        df = self.load_data(data_filepaths)
        model = self.initialize_model(model_name)
        df = self.calculate_scores(df, model)
        statistics = self.calculate_statistics(df)
        
        for metric, score in statistics["Mean Scores"].items():
            print(f"Mean {metric} Score: {score:.4f}")
        print(f"Total Test Cases: {statistics['Total Test Cases']}")
        print(f"Passed Test Cases: {statistics['Passed Test Cases']}")
        print(f"Failed Test Cases: {statistics['Failed Test Cases']}")
        print(f"Percentage Above Threshold: {statistics['Percentage Above Threshold']:.2f}%")
        
        self.save_results(df, statistics, excel_output_filepath, txt_output_filepath)

def main():
    data_filepaths = [
        "EvaluationAndTesting/Testing_data/generated_answers.csv",
        "EvaluationAndTesting/Testing_data/generated_answers_multilingual.csv",
        "EvaluationAndTesting/Testing_data/generated_answers_wrong_vocab_grammar.csv",
        "EvaluationAndTesting/Testing_data/generated_answers_misleading_out_of_context.csv"
    ]
    excel_output_filepath = "EvaluationAndTesting/Evaluation/EvaluationReport.xlsx"
    txt_output_filepath = "EvaluationAndTesting/Evaluation/cummulativeEvaluationReport.txt"
    model_name = 'all-MiniLM-L6-v2'

    evaluator = ModelEvaluator()
    evaluator.evaluate(data_filepaths, model_name, excel_output_filepath, txt_output_filepath)

if __name__ == "__main__":
    main()
