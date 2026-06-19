from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_scrape():
    r = client.post("/api/v1/scrape", json={"url": "https://example.com", "selector": "h1"})
    assert r.status_code == 200
    assert r.json()["status"] == "queued"
    
    r2 = client.post("/api/v1/scrape", json={"url": "bad-url", "selector": "h1"})
    assert r2.status_code == 400

