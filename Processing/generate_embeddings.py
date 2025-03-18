import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load Chunked JSON Data
def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Generate Embeddings for Each Chunk Using Sentence Transformers
def generate_embeddings(chunks, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)  # Load model
    texts = [chunk["content"] for chunk in chunks]
    embeddings = model.encode(texts, convert_to_numpy=True)  # Generate vectors
    return texts, embeddings

# Store Embeddings in FAISS
def store_faiss(embeddings, texts, faiss_index_path="Data/faiss_index"):
    dimension = embeddings.shape[1]  # Get embedding vector size
    index = faiss.IndexFlatL2(dimension)  # Create FAISS index

    # Add embeddings to the FAISS index
    index.add(embeddings)
    
    # Save FAISS index
    faiss.write_index(index, f"{faiss_index_path}.index")

    # Save text metadata
    with open(f"{faiss_index_path}.json", "w", encoding="utf-8") as f:
        json.dump(texts, f)

    print(f" Embeddings stored in FAISS: {faiss_index_path}.index")

# Process JSON Data
file_path = "Data/chunked_data.json"
data = load_json(file_path)

# Generate Embeddings
texts, embeddings = generate_embeddings(data)

# Store in FAISS
store_faiss(embeddings, texts)
