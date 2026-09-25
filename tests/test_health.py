
from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["application"] == "SIGNSYNC"
    assert data["status"] == "running"
    assert data["version"] == "1.0.0"


def test_health_endpoint():
    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.json()

    assert data["application"] == "SIGNSYNC"
    assert data["status"] == "healthy"


def test_swagger_documentation():
    response = client.get("/docs")

    assert response.status_code == 200


def test_openapi_schema():
    response = client.get("/openapi.json")

    assert response.status_code == 200

    data = response.json()

    assert data["info"]["title"] == "SIGNSYNC API"
    assert "/api/health" in data["paths"]
