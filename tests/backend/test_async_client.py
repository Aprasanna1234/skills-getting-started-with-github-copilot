import pytest


@pytest.mark.asyncio
async def test_async_get_activities(async_client):
    resp = await async_client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Chess Club" in data
