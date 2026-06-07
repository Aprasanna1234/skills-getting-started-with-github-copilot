"""
Tests for the POST /activities/{activity_name}/signup endpoint
"""

import pytest


def test_signup_for_activity_success(client, reset_activities):
    """
    Test successful signup for an activity
    """
    # Arrange
    email = "alice@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert data["message"] == f"Signed up {email} for {activity}"


def test_signup_adds_email_to_participants(client, reset_activities):
    """
    Test that signup actually adds the email to the activity's participants list
    """
    # Arrange
    email = "alice@mergington.edu"
    activity = "Chess Club"
    
    # Act
    client.post(f"/activities/{activity}/signup?email={email}")
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    
    # Assert
    assert email in activities_data[activity]["participants"]


def test_signup_for_different_activities(client, reset_activities):
    """
    Test that a student can sign up for different activities
    """
    # Arrange
    email1 = "alice@mergington.edu"
    email2 = "bob@mergington.edu"
    activity1 = "Chess Club"
    activity2 = "Programming Class"
    
    # Act
    client.post(f"/activities/{activity1}/signup?email={email1}")
    client.post(f"/activities/{activity2}/signup?email={email2}")
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    
    # Assert
    assert email1 in activities_data[activity1]["participants"]
    assert email2 in activities_data[activity2]["participants"]


def test_signup_multiple_students_same_activity(client, reset_activities):
    """
    Test that multiple different students can sign up for the same activity
    """
    # Arrange
    emails = ["alice@mergington.edu", "bob@mergington.edu", "charlie@mergington.edu"]
    activity = "Gym Class"
    
    # Act
    for email in emails:
        client.post(f"/activities/{activity}/signup?email={email}")
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    gym_participants = activities_data[activity]["participants"]
    
    # Assert
    for email in emails:
        assert email in gym_participants
    assert email3 in gym_participants
