from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_returns_endpoint():
    response = client.get("/returns", params={"as_of": "2025-06-30"})
    assert response.status_code == 200
    assert "results" in response.json()

def test_exposure_endpoint():
    response = client.get("/exposure", params={"start_date": "2025-04-01", "end_date": "2025-06-30"})
    assert response.status_code == 200
    assert "results" in response.json()
