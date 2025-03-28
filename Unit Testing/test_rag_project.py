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

@pytest.fixture
def scraper():
    return Scraper()

@pytest.fixture
def chunker():
    return chunking

@pytest.fixture
def embedder():
    return embedding

@pytest.fixture
def rag_pipeline():
    return pipeline


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

def test_scraper_invalid_url(scraper):
    url = "invalid_url"
    with pytest.raises(Exception):
        scraper.extract_wikipedia_data(url)
    print("test_scraper_invalid_url passed")

def test_scraper_empty_url(scraper):
    url = ""
    with pytest.raises(ValueError):
        scraper.extract_wikipedia_data(url)
    print("test_scraper_empty_url passed")

def test_chunker(chunker):
    file_path = "Data/combined_Raw_Data.json"
    output_file = "Data/chunked_data.json"
    data = chunker.load_json(file_path)
    full_text = chunker.combine_text(data)
    chunked_data = chunker.chunk_text(full_text)
    transformed_chunked_data = [{"chunk_id": i+1, "content": chunk} for i, chunk in enumerate(chunked_data)]  # Ensure correct transformation
    assert os.path.exists(output_file)
    with open(output_file, 'r') as file:
        saved_data = json.load(file)
    assert transformed_chunked_data == saved_data
    print("test_chunker passed")

def test_chunker_empty_file(chunker):
    file_path = "Data/empty_file.json"
    with open(file_path, 'w') as file:
        json.dump({}, file)
    with pytest.raises(ValueError):
        chunker.load_json(file_path)
    print("test_chunker_empty_file passed")

def test_chunker_invalid_format(chunker):
    file_path = "Data/invalid_format.txt"
    with open(file_path, 'w') as file:
        file.write("This is not JSON format.")
    with pytest.raises(json.JSONDecodeError):
        chunker.load_json(file_path)
    print("test_chunker_invalid_format passed")

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

def test_embedding_empty_data(embedder):
    file_path = "Data/empty_chunked_data.json"
    with open(file_path, 'w') as file:
        json.dump([], file)
    data = embedder.load_json(file_path)
    texts, embeddings = embedder.generate_embeddings(data)
    assert texts == []
    assert embeddings == []
    print("test_embedding_empty_data passed")

def test_rag_pipeline(rag_pipeline):
    query = "What is OpenAI?"
    answer = rag_pipeline.query_rag_pipeline(query)
    assert answer is not None
    print("test_rag_pipeline passed")

def test_rag_pipeline_empty_query(rag_pipeline):
    query = ""
    with pytest.raises(ValueError):
        rag_pipeline.query_rag_pipeline(query)
    print("test_rag_pipeline_empty_query passed")

def test_rag_pipeline_invalid_query(rag_pipeline):
    query = 12345  # Non-string input
    with pytest.raises(TypeError):
        rag_pipeline.query_rag_pipeline(query)
    print("test_rag_pipeline_invalid_query passed")
