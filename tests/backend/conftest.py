import copy

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from src.app import app, activities


_initial_activities = copy.deepcopy(activities)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac


@pytest.fixture
def reset_activities():
    activities.clear()
    activities.update(copy.deepcopy(_initial_activities))
    yield
    activities.clear()
    activities.update(copy.deepcopy(_initial_activities))
