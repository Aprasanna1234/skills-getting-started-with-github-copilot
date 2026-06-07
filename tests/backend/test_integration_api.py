"""
Backend integration tests for the FastAPI application.
"""

import pytest


def test_api_documentation_available(client):
    # Arrange / Act
    response = client.get("/openapi.json")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "info" in data


def test_api_has_title_and_description(client):
    # Arrange / Act
    response = client.get("/openapi.json")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["info"]["title"] == "Mergington High School API"
    assert "extracurricular activities" in data["info"]["description"]


def test_invalid_http_method_on_activities(client, reset_activities):
    # Arrange / Act
    response = client.delete("/activities")

    # Assert
    assert response.status_code == 405


def test_invalid_http_method_on_signup(client, reset_activities):
    # Arrange / Act
    response = client.get("/activities/Chess Club/signup?email=test@example.com")

    # Assert
    assert response.status_code == 405


def test_activities_endpoint_response_content_type(client, reset_activities):
    # Arrange / Act
    response = client.get("/activities")

    # Assert
    assert "application/json" in response.headers.get("content-type", "")


def test_signup_endpoint_response_content_type(client, reset_activities):
    # Arrange / Act
    response = client.post("/activities/Chess Club/signup?email=test@example.com")

    # Assert
    assert "application/json" in response.headers.get("content-type", "")


def test_multiple_activities_consistency(client, reset_activities):
    # Arrange
    email1 = "alice@mergington.edu"
    email2 = "bob@mergington.edu"

    # Act
    client.post(f"/activities/Chess Club/signup?email={email1}")
    client.post(f"/activities/Programming Class/signup?email={email2}")

    # Assert
    data = client.get("/activities").json()
    assert email1 in data["Chess Club"]["participants"]
    assert email2 in data["Programming Class"]["participants"]
    assert len(data["Chess Club"]["participants"]) == 3
    assert len(data["Programming Class"]["participants"]) == 3
    assert len(data["Gym Class"]["participants"]) == 2


def test_activity_descriptions_are_preserved(client, reset_activities):
    # Arrange
    response = client.get("/activities")
    initial_data = response.json()

    # Act
    client.post("/activities/Chess Club/signup?email=alice@mergington.edu")
    updated_data = client.get("/activities").json()

    # Assert
    assert initial_data["Chess Club"]["description"] == updated_data["Chess Club"]["description"]
    assert initial_data["Programming Class"]["description"] == updated_data["Programming Class"]["description"]
    assert initial_data["Gym Class"]["description"] == updated_data["Gym Class"]["description"]


def test_activity_schedule_is_preserved(client, reset_activities):
    # Arrange
    response = client.get("/activities")
    initial_data = response.json()

    # Act
    client.post("/activities/Programming Class/signup?email=student@mergington.edu")
    updated_data = client.get("/activities").json()

    # Assert
    assert initial_data["Chess Club"]["schedule"] == updated_data["Chess Club"]["schedule"]
    assert initial_data["Programming Class"]["schedule"] == updated_data["Programming Class"]["schedule"]


def test_max_participants_never_changes(client, reset_activities):
    # Arrange
    response = client.get("/activities")
    initial_data = response.json()

    # Act
    for i in range(5):
        client.post(f"/activities/Gym Class/signup?email=student{i}@mergington.edu")
    updated_data = client.get("/activities").json()

    # Assert
    assert initial_data["Gym Class"]["max_participants"] == updated_data["Gym Class"]["max_participants"]
    assert updated_data["Gym Class"]["max_participants"] == 30
