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
        index = faiss.read_index(f"{faiss_index_path}.index") 
        with open(f"{faiss_index_path}.json", "r", encoding="utf-8") as f:
            texts = json.load(f)  
        return index, texts

    #  Generate Embedding for Query
    def get_query_embedding(query, model_name="all-MiniLM-L6-v2"):
        model = SentenceTransformer(model_name)  
        return model.encode(query, convert_to_numpy=True)  

    def search_faiss(query_embedding, index, texts, top_k=3):
        query_embedding = np.array([query_embedding], dtype=np.float32)  
        _, indices = index.search(query_embedding, top_k)  
        retrieved_texts = [texts[i] for i in indices[0] if i < len(texts)]  
        return retrieved_texts


    def ask_gemini(query, context, max_output_tokens=500):
        """Generate answer using Gemini with a token limit to prevent errors."""
        
        genai.configure(api_key=os.getenv("API_KEY"))  
        
        model = genai.GenerativeModel("models/gemini-1.5-flash-8b")
        

        prompt = f"Context:\n{context}\n\nUser Question: {query}\nAnswer:"
        
        try:
            response = model.generate_content(
                prompt, generation_config={"max_output_tokens": max_output_tokens}
            )
            return response.text 
        except Exception as e:
            print(f" Gemini API Error: {e}")
            return "Error: Unable to generate an answer."


    #  Main Function to Answer Query
    def query_rag_pipeline(query, faiss_index_path="Data/faiss_index"):
        index, texts = pipeline.load_faiss(faiss_index_path) 
        query_embedding = pipeline.get_query_embedding(query)  
        retrieved_chunks = pipeline.search_faiss(query_embedding, index, texts) 
        context = "\n".join(retrieved_chunks) 
        answer = pipeline.ask_gemini(query, context)  

        return answer

