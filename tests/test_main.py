from fastapi.testclient import TestClient

import src.main as service

client = TestClient(service.app)


def setup_function():
    service.plans.clear()


def test_health_and_readiness():
    assert client.get("/healthz").status_code == 200
    response = client.get("/readyz")
    assert response.status_code == 200
    assert response.json()["capacity"] == service.MAX_JOBS


def test_create_and_retrieve_plan():
    response = client.post(
        "/v1/plans",
        json={"url": "https://Example.com/docs#section", "selector": "main h1"},
    )
    assert response.status_code == 201
    plan = response.json()
    assert plan["url"] == "https://example.com/docs"
    assert plan["host"] == "example.com"
    assert plan["status"] == "planned"
    fetched = client.get(f"/v1/plans/{plan['id']}")
    assert fetched.status_code == 200
    assert fetched.json() == plan


def test_rejects_unsafe_urls_and_blank_selectors():
    for url in [
        "http://example.com",
        "https://localhost/x",
        "https://127.0.0.1/x",
        "https://user:secret@example.com/x",
    ]:
        response = client.post("/v1/plans", json={"url": url, "selector": "h1"})
        assert response.status_code == 422
    assert client.post(
        "/v1/plans", json={"url": "https://example.com", "selector": "   "}
    ).status_code == 422


def test_capacity_fails_closed(monkeypatch):
    monkeypatch.setattr(service, "MAX_JOBS", 1)
    assert client.post(
        "/v1/plans", json={"url": "https://example.com/one", "selector": "h1"}
    ).status_code == 201
    assert client.post(
        "/v1/plans", json={"url": "https://example.com/two", "selector": "h2"}
    ).status_code == 503
