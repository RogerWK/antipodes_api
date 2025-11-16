import pytest
from fastapi.testclient import TestClient
from app.main import app
import pandas as pd
from unittest.mock import patch

client = TestClient(app)

# Sample DataFrames to mock your Excel data
sample_returns_df = pd.DataFrame({
    "VehicleID": ["A", "B"],
    "Date": ["2025-06-01", "2025-06-02"],
    "Return": [0.01, 0.02],
    "FundID": ["FUNDA", "FUNDA"],
    "BenchID": ["BENCHA", "BENCHA"]
})

sample_exposure_df = pd.DataFrame({
    "IndexDate": ["2025-04-01", "2025-04-02"],
    "Weight": [0.5, 0.5],
    "IndexID": ["BENCHA", "BENCHA"]
})

@pytest.fixture(autouse=True)
def mock_data_loading():
    # Patch the functions in main.py that load Excel data
    with patch("app.main.load_returns_data", return_value=sample_returns_df):
        with patch("app.main.load_exposure_data", return_value=sample_exposure_df):
            yield


def test_returns_endpoint():
    response = client.get("/returns", params={"as_of": "2025-06-30"})
    assert response.status_code == 200
    json_data = response.json()
    assert "results" in json_data
    assert isinstance(json_data["results"], list)
    assert len(json_data["results"]) > 0


def test_exposure_endpoint():
    response = client.get("/exposure", params={"start_date": "2025-04-01", "end_date": "2025-06-30"})
    assert response.status_code == 200
    json_data = response.json()
    assert "results" in json_data
    assert isinstance(json_data["results"], list)
    assert len(json_data["results"]) > 0
