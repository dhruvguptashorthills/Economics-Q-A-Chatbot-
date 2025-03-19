import json
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

class chunking():
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
        return " ".join(chunking.clean_text(entry["content"]) for entry in data)

    # Chunk text using LangChain's RecursiveCharacterTextSplitter
    def chunk_text(text, chunk_size=1000, chunk_overlap=200):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n","\n",". "] 
        )
        chunks = text_splitter.split_text(text)
        

        cleaned_chunks = [chunk.lstrip(".?! \n") for chunk in chunks]
        
        return cleaned_chunks
    
    # Save Chunked Data to JSON
    def save_json(data, output_file):
        data = [{"chunk_id": i+1, "content": data} for i, data in enumerate(chunks)]

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

# Process JSON
file_path = "Data/combined_Raw_Data.json"  # Update with your JSON file path
output_file = "Data/chunked_data.json"

data = chunking.load_json(file_path)
full_text = chunking.combine_text(data)
chunked_data = chunking.chunk_text(full_text)


chunking.save_json(chunked_data, output_file)

print(f"Chunking complete. Data saved to {output_file}")
