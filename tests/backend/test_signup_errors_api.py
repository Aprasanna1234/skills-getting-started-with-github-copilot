"""
Backend tests for signup error and edge case handling.
"""

import pytest


def test_signup_for_nonexistent_activity(client, reset_activities):
    # Arrange
    email = "alice@mergington.edu"

    # Act
    response = client.post(f"/activities/Nonexistent Activity/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_duplicate_enrollment(client, reset_activities):
    # Arrange
    email = "alice@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert f"{email} is already enrolled in {activity}" in response.json()["detail"]


def test_signup_for_already_enrolled_initial_participant(client, reset_activities):
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert f"{email} is already enrolled in {activity}" in response.json()["detail"]


def test_signup_activity_at_capacity(client, reset_activities):
    # Arrange
    activity = "Chess Club"
    emails = [f"student{i}@mergington.edu" for i in range(10)]
    for email in emails:
        client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity}/signup?email=extra@mergington.edu")

    # Assert
    assert response.status_code == 400
    assert "at full capacity" in response.json()["detail"]


def test_signup_case_sensitive_activity_names(client, reset_activities):
    # Arrange
    email = "alice@mergington.edu"

    # Act
    response = client.post(f"/activities/chess club/signup?email={email}")

    # Assert
    assert response.status_code == 404
