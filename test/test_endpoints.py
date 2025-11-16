import pytest
from fastapi.testclient import TestClient
import pandas as pd
from app.main import app
from app.data_processing import cumulative_returns_and_alpha, exposure_difference

client = TestClient(app)

# -----------------------------
# Unit tests for core functions
# -----------------------------

def test_cumulative_returns_and_alpha():
    # Mock returns data
    df = pd.DataFrame({
        "Date": pd.date_range("2025-01-01", periods=6, freq="M"),
        "VehicleID": ["FUNDA","BENCHA","FUNDA","BENCHA","FUNDA","BENCHA"],
        "Return": [0.02, 0.015, 0.03, 0.025, -0.01, -0.005]
    })

    result = cumulative_returns_and_alpha(
        df,
        as_of_date="2025-06-30",
        vehicle_col="VehicleID",
        return_col="Return",
        date_col="Date",
        month_period=[3,6],
        fund_id="FUNDA",
        bench_id="BENCHA",
        na_strategy="keep"
    )

    assert isinstance(result, list)
    assert "FundReturn" in result[0]
    assert "BenchmarkReturn" in result[0]
    assert "Alpha" in result[0]


def test_exposure_difference():
    df = pd.DataFrame({
        "IndexDate": pd.to_datetime(["2025-04-01","2025-06-30","2025-04-01","2025-06-30"]),
        "IndexID": ["BENCHA","BENCHA","BENCHA","BENCHA"],
        "AntipodesRegion": ["Asia","Asia","Europe","Europe"],
        "Weight": [0.40,0.45,0.60,0.55]
    })

    result = exposure_difference(
        df,
        start_date="2025-04-01",
        end_date="2025-06-30",
        date_col="IndexDate",
        weight_col="Weight",
        index_id="BENCHA",
        na_strategy="keep"
    )

    assert isinstance(result, list)
    assert result[0]["Difference"] == pytest.approx(0.05, rel=1e-3)
    assert result[1]["Difference"] == pytest.approx(-0.05, rel=1e-3)


# -----------------------------
# Integration tests for API
# -----------------------------

def test_returns_endpoint(monkeypatch):
    # Patch global returns_df in app.main
    import app.main
    app.main.returns_df = pd.DataFrame({
        "Date": pd.date_range("2025-01-01", periods=6, freq="M"),
        "VehicleID": ["FUNDA","BENCHA","FUNDA","BENCHA","FUNDA","BENCHA"],
        "Return": [0.02, 0.015, 0.03, 0.025, -0.01, -0.005]
    })

    response = client.get("/returns", params={"as_of":"2025-06-30"})
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)


def test_exposure_endpoint(monkeypatch):
    import app.main
    app.main.constituents_df = pd.DataFrame({
        "IndexDate": pd.to_datetime(["2025-04-01","2025-06-30","2025-04-01","2025-06-30"]),
        "IndexID": ["BENCHA","BENCHA","BENCHA","BENCHA"],
        "AntipodesRegion": ["Asia","Asia","Europe","Europe"],
        "Weight": [0.40,0.45,0.60,0.55]
    })

    response = client.get("/exposure", params={"start_date":"2025-04-01","end_date":"2025-06-30"})
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert isinstance(data["results"], list)
    assert data["results"][0]["StartWeight"] == pytest.approx(0.40, rel=1e-3)
