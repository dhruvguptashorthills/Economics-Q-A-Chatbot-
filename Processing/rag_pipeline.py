import json
import faiss
import numpy as np
from dotenv import load_dotenv
import os
load_dotenv()
from sentence_transformers import SentenceTransformer
import google.generativeai as genai

class pipeline():
    #  Load FAISS Index
    def load_faiss(faiss_index_path="Data/faiss_index"):
        index = faiss.read_index(f"{faiss_index_path}.index")  # Load FAISS index
        with open(f"{faiss_index_path}.json", "r", encoding="utf-8") as f:
            texts = json.load(f)  # Load text metadata
        return index, texts

    #  Generate Embedding for Query
    def get_query_embedding(query, model_name="all-MiniLM-L6-v2"):
        model = SentenceTransformer(model_name)  # Load embedding model
        return model.encode(query, convert_to_numpy=True)  # Get vector

    #  Search FAISS for Relevant Chunks
    def search_faiss(query_embedding, index, texts, top_k=3):
        query_embedding = np.array([query_embedding], dtype=np.float32)  # Convert to NumPy array
        _, indices = index.search(query_embedding, top_k)  # Search FAISS
        retrieved_texts = [texts[i] for i in indices[0] if i < len(texts)]  # Get top chunks 
        return retrieved_texts


    def ask_gemini(query, context, max_output_tokens=500):
        """Generate answer using Gemini with a token limit to prevent errors."""
        
        # Configure Gemini API Key
        genai.configure(api_key=os.getenv("API_KEY"))  
        
        # Load Gemini model
        model = genai.GenerativeModel("models/gemini-1.5-flash-8b")
        

        # Construct the prompt
        prompt = f"Context:\n{context}\n\nUser Question: {query}\nAnswer:"
        
        try:
            response = model.generate_content(
                prompt, generation_config={"max_output_tokens": max_output_tokens}
            )
            return response.text  # Return the generated answer

        except Exception as e:
            print(f" Gemini API Error: {e}")
            return "Error: Unable to generate an answer."


    #  Main Function to Answer Query
    def query_rag_pipeline(query, faiss_index_path="Data/faiss_index"):
        index, texts = pipeline.load_faiss(faiss_index_path)  # Load FAISS
        query_embedding = pipeline.get_query_embedding(query)  # Convert query to vector
        retrieved_chunks = pipeline.search_faiss(query_embedding, index, texts)  # Retrieve context
        context = "\n".join(retrieved_chunks)  # Combine top chunks
        answer = pipeline.ask_gemini(query, context)  # Get final answer from Gemini
        # print("\n🔹 Context:", context)
        return answer

# #  Example Query
# query = "What is austrian school of economics?"
# response = pipeline.query_rag_pipeline(query)
# print("\nAnswer:", response)
