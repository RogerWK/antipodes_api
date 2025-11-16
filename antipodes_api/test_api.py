import pytest
from httpx import AsyncClient
from app.main import app
@pytest.mark.asyncio
async def test_returns_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/returns?as_of=2025-06-30&month_period=1&month_period=3"
        )
    assert response.status_code == 200
    assert "results" in response.json()

@pytest.mark.asyncio
async def test_exposure_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/exposure?start_date=2025-04-01&end_date=2025-06-30"
        )
    assert response.status_code == 200
    assert "results" in response.json()
