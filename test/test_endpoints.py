import pytest
from fastapi.testclient import TestClient
from app.main import app
import pandas as pd

client = TestClient(app)

@pytest.fixture
def sample_returns_df(monkeypatch):
    # Mock your data loading function to return a sample DataFrame
    sample_df = pd.DataFrame({
        "VehicleID": ["A", "B"],
        "Date": ["2025-06-01", "2025-06-02"],
        "Return": [0.01, 0.02],
        "FundID": ["FUNDA", "FUNDA"],
        "BenchID": ["BENCHA", "BENCHA"]
    })
    # Monkeypatch the function in main.py that loads the Excel
    monkeypatch.setattr("app.main.load_returns_data", lambda: sample_df)
    return sample_df

def test_returns_endpoint(sample_returns_df):
    response = client.get("/returns", params={"as_of": "2025-06-30"})
    assert response.status_code == 200
    assert "results" in response.json()
