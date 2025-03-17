# Economics Q&A Chatbot

## Overview

The **Economics Q&A Chatbot** is a Retrieval-Augmented Generation (RAG)-based chatbot that provides answers to questions using economics-related data. The system scrapes articles from a designated website, processes the data into vector embeddings, and utilises an LLM (such as Llama or Open AI) to generate responses.

## Functionality

1. **Web Scraping & Data Collection**

   - Extracts articles from predefined URLs using [Scraper.py](https://github.com/dhruvguptashorthills/Economics-Q-A-Chatbot-/blob/main/Scraper/Scraper.py).
   - Saves articles as text files and compiles structured JSON data.

2. **Text Processing & Chunking**

   - Cleans and splits articles into manageable chunks using [chunker.py](https://github.com/dhruvguptashorthills/Economics-Q-A-Chatbot-/blob/main/Processing/chunker.py).
   - Saves chunked data to a JSON file for embedding.

3. **Embedding Generation & Storage in FAISS**

   - Converts text chunks into embeddings using [generate\_embeddings.py](https://github.com/dhruvguptashorthills/Economics-Q-A-Chatbot-/blob/main/Processing/generate_embeddings.py).
   - Stores embeddings in FAISS for fast retrieval.

4. **Query Processing & Retrieval (RAG Pipeline)**

   - Searches FAISS for relevant text chunks using [rag\_pipeline.py](https://github.com/dhruvguptashorthills/Economics-Q-A-Chatbot-/blob/main/Processing/rag_pipeline.py).
   - Constructs a context-aware prompt for the AI model and generates an answer.

5. **Question Generation & Golden Set Creation**

   - Generates questions and answers using [generate\_Q&A\_set.py](https://github.com/dhruvguptashorthills/Economics-Q-A-Chatbot-/blob/main/EvaluationAndTesting/generate_Q%26A_set.py).
   - Saves compiled Q&A sets for evaluation.

6. **Model Evaluation & Performance Metrics**

   - Compares generated responses with golden set answers using [Evaluate\_model.py](https://github.com/dhruvguptashorthills/Economics-Q-A-Chatbot-/blob/main/EvaluationAndTesting/Evaluate_model.py).
   - Outputs an evaluation report.

7. **Streamlit User Interface**

   - Provides a real-time interactive UI via [app.py](https://github.com/dhruvguptashorthills/Economics-Q-A-Chatbot-/blob/main/app.py).
   - Logs user queries for tracking interactions.

## Project Structure

```
Economics-Q-A-Chatbot/
│── data/               # Scraped articles and processed text
│── embeddings/         # Stored vector embeddings
│── models/             # Pretrained LLM and RAG model
│── notebooks/          # Jupyter notebooks for development and testing
│── scripts/            # Python scripts for scraping, processing, and inference
│── app.py              # Streamlit app entry point
│── requirements.txt    # Dependencies
│── README.md           # Project documentation
```

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/dhruvguptashorthills/Economics-Q-A-Chatbot-.git
   cd Economics-Q-A-Chatbot-
   ```

2. **Create a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Data Scraping

Run the web scraper to collect economic articles:

```bash
python scripts/scraper.py
```

### 2. Data Processing & Chunking

Clean and split the scraped text into manageable chunks:

```bash
python scripts/chunker.py
```

### 3. Data Embedding Generation

Convert chunked text into vector embeddings:

```bash
python scripts/embedder.py
```

### 4. Start the Chatbot App

Launch the local Streamlit interface:

```bash
streamlit run app.py
```

## Evaluation

The chatbot is evaluated using a predefined **golden set** of 1000+ Q&A pairs. To test accuracy:

```bash
python scripts/evaluate.py
```

## Technologies Used

- **Python** (Data processing & LLM integration)
- **BeautifulSoup, Scrapy** (Web scraping)
- **FAISS** (Vector database)
- **OpenAI/Llama Models** (LLM-based responses)
- **Streamlit** (User interface)
- **Azure Blob Storage** (Data storage)

## License

This project is licensed under the MIT License.

