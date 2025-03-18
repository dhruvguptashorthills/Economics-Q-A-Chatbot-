import json
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load JSON File
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Clean Text (e.g., remove LaTeX expressions)
def clean_text(text):
    text = re.sub(r"{\\displaystyle\\s*\\textstyle\s*[^}]+}", "", text)  
    text = re.sub(r"\s+", " ", text).strip()  
    return text

# Combine all text from JSON into one large string
def combine_text(data):
    return " ".join(clean_text(entry["content"]) for entry in data)

# Chunk text using LangChain's RecursiveCharacterTextSplitter
def chunk_text(text, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n","\n",". ", "? ", "! "]  # Ensures sentence-based splitting
    )
    chunks = text_splitter.split_text(text)
    

    cleaned_chunks = [chunk.lstrip(".?! \n") for chunk in chunks]
    
    return cleaned_chunks
# Save Chunked Data to JSON
def save_json(data, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Process JSON
file_path = "Data/combined_Raw_Data.json"  # Update with your JSON file path
output_file = "Data/chunked_data.json"

data = load_json(file_path)
full_text = combine_text(data)
chunks = chunk_text(full_text)

# Convert to JSON format
chunked_data = [{"chunk_id": i+1, "content": chunk} for i, chunk in enumerate(chunks)]

save_json(chunked_data, output_file)

print(f"Chunking complete. Data saved to {output_file}")
