from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


def test_get_posts():
    response = client.get("/posts")

    assert response.status_code == 200

    assert isinstance(response.json(), list)


def test_get_suggestions():
    response = client.get("/suggestions")

    assert response.status_code == 200

    assert isinstance(response.json(), list)


def test_get_ai_usage():
    response = client.get("/ai-usage")

    assert response.status_code == 200

    data = response.json()

    assert "total_operations" in data
    assert "records" in data