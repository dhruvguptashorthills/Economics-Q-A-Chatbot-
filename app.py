import streamlit as st
from Processing.rag_pipeline import pipeline
import json
import os
from datetime import datetime

class EconomicsQASystem:
    def __init__(self):
        self.log_file = "Logging/user_queries_log.json"
        st.set_page_config(page_title="Economics Q&A System")
        self.setup_ui()

    def setup_ui(self):
        st.title("Economics Q&A System")
        self.query = st.text_input("Enter your question:", on_change=self.on_query_change)
        if st.session_state.get("button_pressed") or st.button("Get Answer"):
            self.handle_query()

    def on_query_change(self):
        st.session_state.update({"button_pressed": True})

    def handle_query(self):
        if self.query:
            with st.spinner("Fetching answer..."):
                try:
                    response = pipeline.query_rag_pipeline(self.query)
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    self.save_to_json(timestamp, self.query, response)
                except RuntimeError:
                    response = "An error occurred while fetching the answer."
                self.display_answer(response)
            st.session_state["button_pressed"] = False
        else:
            st.warning("Please enter a question.")

    def save_to_json(self, timestamp, question, answer):
        data = []
        if os.path.exists(self.log_file):
            with open(self.log_file, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
        data.append({"timestamp": timestamp, "question": question, "answer": answer})
        with open(self.log_file, "w") as file:
            json.dump(data, file, indent=4)

    def display_answer(self, response):
        st.subheader("Answer:")
        st.markdown(f'<div style="border:1px solid black; padding:10px; border-radius:5px; max-height:500px; overflow:auto;">{response}</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    EconomicsQASystem()