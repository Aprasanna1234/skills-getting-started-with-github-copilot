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


def test_get_activities_returns_all_activities(client):
    # Arrange
    expected_activities = {"Chess Club", "Programming Class", "Gym Class"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert expected_activities.issubset(set(data.keys()))


def test_get_activities_returns_correct_activity_structure(client):
    # Arrange
    activity_name = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    chess_club = data[activity_name]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_get_activities_includes_initial_participants(client):
    # Arrange
    expected_emails = {
        "Chess Club": ["michael@mergington.edu", "daniel@mergington.edu"],
        "Programming Class": ["emma@mergington.edu", "sophia@mergington.edu"],
        "Gym Class": ["john@mergington.edu", "olivia@mergington.edu"],
    }

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    for activity_name, emails in expected_emails.items():
        for email in emails:
            assert email in data[activity_name]["participants"]


def test_get_activities_returns_correct_max_participants(client):
    # Arrange
    expected_capacity = {"Chess Club": 12, "Programming Class": 20, "Gym Class": 30}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    for activity_name, max_participants in expected_capacity.items():
        assert data[activity_name]["max_participants"] == max_participants


def test_signup_flow(client, reset_activities):
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    activities_data = client.get("/activities").json()
    assert email in activities_data[activity]["participants"]
