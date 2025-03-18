import streamlit as st
from Processing.rag_pipeline import query_rag_pipeline  
import json
import os
from datetime import datetime



json_file = "Logging/user_queries_log.json"

def save_to_json(timestamp, question, answer):
    data = []
    
    if os.path.exists(json_file):
        with open(json_file, "r") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []  
    
    data.append({"timestamp": timestamp, "question": question, "answer": answer})
    
    with open(json_file, "w") as file:
        json.dump(data, file, indent=4)

st.title("Economics Q&A System")

query = st.text_input("Enter your question:")
if st.button("Get Answer"):
    if query:
        with st.spinner("Fetching answer..."):
            try:
                response = query_rag_pipeline(query)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                save_to_json(timestamp, query, response)

            except RuntimeError:
                response = "An error occurred while fetching the answer."

        st.subheader("Answer:")
        st.write(response)
    else:
        st.warning("Please enter a question.")
