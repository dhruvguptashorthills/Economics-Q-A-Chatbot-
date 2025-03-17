import pandas as pd
from sentence_transformers import SentenceTransformer, util

# Load the dataset with generated answers
df = pd.read_csv("EvaluationAndTesting/Testing_data/generated_answers.csv")


# Semantic Similarity Score
model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_similarity(pred, truth):
    emb1 = model.encode(pred, convert_to_tensor=True)
    emb2 = model.encode(truth, convert_to_tensor=True)
    return util.pytorch_cos_sim(emb1, emb2).item()

df["Semantic_Similarity"] = df.apply(lambda row: semantic_similarity(row["generated_answer"], row["answer"]), axis=1)
semantic_score = df["Semantic_Similarity"].mean()
print(f"Mean Semantic Similarity Score: {semantic_score:.4f}")

num_cases_above_threshold = df[df["Semantic_Similarity"] > 0.5].shape[0]
percentage_above_threshold = (num_cases_above_threshold / len(df)) * 100
print(f"Percentage of test cases above threshold: {percentage_above_threshold:.2f}%")

df.to_csv("EvaluationAndTesting/Evaluation/EvaluationReport.csv", index=False)

# Store all scores in a text file
with open("EvaluationAndTesting/Evaluation/CummulativeEvaluationReport.txt", "w") as report_file:
    report_file.write(f"Mean Semantic Similarity Score: {semantic_score:.4f}\n")
    report_file.write(f"Percentage of test cases above threshold: {percentage_above_threshold:.2f}%")
