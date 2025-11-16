import pytest
import pandas as pd
from fastapi.testclient import TestClient
from app.main import app

# --- Sample DataFrames for testing ---
sample_returns_df = pd.DataFrame({
    "VehicleID": ["A", "B"],
    "Date": ["2025-06-01", "2025-06-02"],
    "Return": [0.01, 0.02],
    "FundID": ["FUNDA", "FUNDA"],
    "BenchID": ["BENCHA", "BENCHA"]
})

sample_exposure_df = pd.DataFrame({
    "IndexDate": ["2025-04-01", "2025-05-01"],
    "Weight": [0.5, 0.5],
    "IndexID": ["BENCHA", "BENCHA"]
})

# Dependency overrides
def mock_returns_data():
    return sample_returns_df

def mock_exposure_data():
    return sample_exposure_df

app.dependency_overrides = {
    "get_returns_data": mock_returns_data,
    "get_exposure_data": mock_exposure_data
}

client = TestClient(app)

def test_returns_endpoint():
    response = client.get("/returns", params={"as_of": "2025-06-30"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_exposure_endpoint():
    response = client.get("/exposure", params={"start_date": "2025-04-01", "end_date": "2025-06-30"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
