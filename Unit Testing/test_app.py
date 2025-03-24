import pytest
import os
import sys
from flask import Flask
from flask.testing import FlaskClient


miniproject_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(miniproject_path)
from app import create_app

@pytest.fixture
def app() -> Flask:
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    return app

@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()

def test_home_page(client: FlaskClient):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Welcome to the Home Page" in response.data
    print("test_home_page passed")

def test_query_rag(client: FlaskClient):
    query = {"query": "What is OpenAI?"}
    response = client.post("/query", json=query)
    assert response.status_code == 200
    data = response.get_json()
    assert "answer" in data
    assert data["answer"] is not None
    print("test_query_rag passed")
