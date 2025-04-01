# backend/tests/test_api.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_text_processing():
    response = client.post("/api/process", json={"text": "مرحبا بالعالم"})
    assert response.status_code == 200
    assert "result" in response.json()