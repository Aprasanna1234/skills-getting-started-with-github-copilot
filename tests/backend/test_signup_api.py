"""
Backend tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest


def test_signup_for_activity_success(client, reset_activities):
    # Arrange
    email = "alice@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Signed up {email} for {activity}"


def test_signup_adds_email_to_participants(client, reset_activities):
    # Arrange
    email = "alice@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    activities_data = client.get("/activities").json()
    assert email in activities_data[activity]["participants"]


def test_signup_for_different_activities(client, reset_activities):
    # Arrange
    email1 = "alice@mergington.edu"
    email2 = "bob@mergington.edu"

    # Act
    response1 = client.post(f"/activities/Chess Club/signup?email={email1}")
    response2 = client.post(f"/activities/Programming Class/signup?email={email2}")

    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    activities_data = client.get("/activities").json()
    assert email1 in activities_data["Chess Club"]["participants"]
    assert email2 in activities_data["Programming Class"]["participants"]


def test_signup_multiple_students_same_activity(client, reset_activities):
    # Arrange
    email1 = "alice@mergington.edu"
    email2 = "bob@mergington.edu"
    email3 = "charlie@mergington.edu"
    activity = "Gym Class"

    # Act
    response1 = client.post(f"/activities/{activity}/signup?email={email1}")
    response2 = client.post(f"/activities/{activity}/signup?email={email2}")
    response3 = client.post(f"/activities/{activity}/signup?email={email3}")

    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response3.status_code == 200
    participants = client.get("/activities").json()[activity]["participants"]
    assert email1 in participants
    assert email2 in participants
    assert email3 in participants
