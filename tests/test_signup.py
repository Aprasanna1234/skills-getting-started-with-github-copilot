"""
Tests for the POST /activities/{activity_name}/signup endpoint
"""

import pytest


def test_signup_for_activity_success(client, reset_activities):
    """
    Test successful signup for an activity
    """
    email = "alice@mergington.edu"
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Signed up {email} for Chess Club"


def test_signup_adds_email_to_participants(client, reset_activities):
    """
    Test that signup actually adds the email to the activity's participants list
    """
    email = "alice@mergington.edu"
    
    # Sign up
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response.status_code == 200
    
    # Verify email is in participants
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email in activities_data["Chess Club"]["participants"]


def test_signup_for_different_activities(client, reset_activities):
    """
    Test that a student can sign up for different activities
    """
    email1 = "alice@mergington.edu"
    email2 = "bob@mergington.edu"
    
    # Sign up for Chess Club
    response1 = client.post(f"/activities/Chess Club/signup?email={email1}")
    assert response1.status_code == 200
    
    # Sign up for Programming Class
    response2 = client.post(f"/activities/Programming Class/signup?email={email2}")
    assert response2.status_code == 200
    
    # Verify both signups worked
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert email1 in activities_data["Chess Club"]["participants"]
    assert email2 in activities_data["Programming Class"]["participants"]


def test_signup_multiple_students_same_activity(client, reset_activities):
    """
    Test that multiple different students can sign up for the same activity
    """
    email1 = "alice@mergington.edu"
    email2 = "bob@mergington.edu"
    email3 = "charlie@mergington.edu"
    
    # Sign up multiple students
    response1 = client.post(f"/activities/Gym Class/signup?email={email1}")
    response2 = client.post(f"/activities/Gym Class/signup?email={email2}")
    response3 = client.post(f"/activities/Gym Class/signup?email={email3}")
    
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response3.status_code == 200
    
    # Verify all are in participants
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    gym_participants = activities_data["Gym Class"]["participants"]
    assert email1 in gym_participants
    assert email2 in gym_participants
    assert email3 in gym_participants
