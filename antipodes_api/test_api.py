import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app
from httpx import ASGITransport

@pytest.mark.asyncio
async def test_returns_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/returns", params={"as_of": "2025-06-30"})
        assert response.status_code == 200
        assert "results" in response.json()


@pytest.mark.asyncio
async def test_exposure_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/exposure", params={"start_date": "2025-04-01", "end_date": "2025-06-30"})
        assert response.status_code == 200
        assert "results" in response.json()
