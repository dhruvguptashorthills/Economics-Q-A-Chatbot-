import pytest
import os
import sys
import json
miniproject_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(miniproject_path)
from Scraper.Scraper import Scraper
from Processing.chunker import chunking
from Processing.generate_embeddings import embedding
from Processing.rag_pipeline import pipeline
from EvaluationAndTesting.Evaluate_model import ModelEvaluator

@pytest.fixture
def scraper():
    return Scraper()

@pytest.fixture
def chunker():
    return chunking()

@pytest.fixture
def embedder():
    return embedding()

@pytest.fixture
def rag_pipeline():
    return pipeline()


def test_scraper(scraper):
    url = "https://en.wikipedia.org/wiki/OpenAI"
    title, content = scraper.extract_wikipedia_data(url)
    assert title is not None
    assert content is not None
    filename = scraper.save_article_to_file(title, content)
    assert os.path.exists(filename)
    with open(filename, 'r') as file:
        saved_content = file.read()
    assert content in saved_content
    print("test_scraper passed")

def test_chunker(chunker):
    file_path = "Data/combined_Raw_Data.json"
    output_file = "Data/chunked_data.json"
    data = chunker.load_json(file_path)
    full_text = chunker.combine_text(data)
    chunked_data = chunker.chunk_text(full_text)
    chunker.save_json(chunked_data, output_file)
    assert os.path.exists(output_file)
    with open(output_file, 'r') as file:
        saved_data = json.load(file)
    assert chunked_data == saved_data
    print("test_chunker passed")

def test_embedding(embedder):
    file_path = "Data/chunked_data.json"
    data = embedder.load_json(file_path)
    texts, embeddings = embedder.generate_embeddings(data)
    embedder.store_faiss(embeddings, texts)
    assert os.path.exists("Data/faiss_index.index")
    assert os.path.exists("Data/faiss_index.json")
    with open("Data/faiss_index.json", 'r') as file:
        saved_data = json.load(file)
    assert texts == saved_data
    print("test_embedding passed")

def test_rag_pipeline(rag_pipeline):
    query = "What is OpenAI?"
    answer = rag_pipeline.query_rag_pipeline(query)
    assert answer is not None
    print("test_rag_pipeline passed")
