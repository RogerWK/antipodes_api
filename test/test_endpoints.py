import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_exposure_endpoint(monkeypatch):
    import pandas as pd
    from app.data_processing import load_excel_data

    # Mock data
    returns_df = pd.DataFrame()
    constituents_df = pd.DataFrame({
        "IndexID": ["BENCHA"],
        "AntipodesRegion": ["RegionA"],
        "Weight": [0.5],
        "IndexDate": pd.to_datetime(["2025-06-30"])
    })

    # Patch load_excel_data
    monkeypatch.setattr("app.main.load_excel_data", lambda filepath: (returns_df, constituents_df))

    from app.main import startup_event
    startup_event()

    response = client.get("/exposure?start_date=2025-06-30&end_date=2025-06-30")
    assert response.status_code == 200
    assert "results" in response.json()
