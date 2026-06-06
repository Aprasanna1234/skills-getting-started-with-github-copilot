"""
Tests for error cases and edge cases in the POST /activities/{activity_name}/signup endpoint
"""

import pytest


def test_signup_for_nonexistent_activity(client, reset_activities):
    """
    Test that signing up for a non-existent activity returns 404
    """
    email = "alice@mergington.edu"
    response = client.post(f"/activities/Nonexistent Activity/signup?email={email}")
    
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_signup_duplicate_enrollment(client, reset_activities):
    """
    Test that a student cannot sign up twice for the same activity
    """
    email = "alice@mergington.edu"
    
    # First signup should succeed
    response1 = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response1.status_code == 200
    
    # Second signup with same email should fail
    response2 = client.post(f"/activities/Chess Club/signup?email={email}")
    assert response2.status_code == 400
    data = response2.json()
    assert f"{email} is already enrolled in Chess Club" in data["detail"]


def test_signup_for_already_enrolled_initial_participant(client, reset_activities):
    """
    Test that initial participants cannot enroll again
    """
    email = "michael@mergington.edu"  # Already in Chess Club
    
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    
    assert response.status_code == 400
    data = response.json()
    assert f"{email} is already enrolled in Chess Club" in data["detail"]


def test_signup_activity_at_capacity(client, reset_activities):
    """
    Test that an activity at full capacity rejects new signups
    """
    # Chess Club has max_participants of 12, with 2 initial participants
    # Fill it up with 10 more students
    emails = [f"student{i}@mergington.edu" for i in range(10)]
    
    for email in emails:
        response = client.post(f"/activities/Chess Club/signup?email={email}")
        assert response.status_code == 200
    
    # Now the activity should be at capacity (2 + 10 = 12)
    # Try to add one more
    new_email = "extra@mergington.edu"
    response = client.post(f"/activities/Chess Club/signup?email={new_email}")
    
    assert response.status_code == 400
    data = response.json()
    assert "at full capacity" in data["detail"]


def test_signup_large_activity_not_full(client, reset_activities):
    """
    Test that activities with large capacity can accommodate many students
    """
    # Gym Class has max_participants of 30, with 2 initial participants
    # Try to sign up 28 more (total 30)
    emails = [f"student{i}@mergington.edu" for i in range(28)]
    
    for email in emails:
        response = client.post(f"/activities/Gym Class/signup?email={email}")
        assert response.status_code == 200
    
    # Verify all are enrolled
    activities_response = client.get("/activities")
    activities_data = activities_response.json()
    assert len(activities_data["Gym Class"]["participants"]) == 30


def test_signup_empty_email_parameter(client, reset_activities):
    """
    Test that signing up with empty email parameter is handled
    """
    response = client.post(f"/activities/Chess Club/signup?email=")
    
    # Should either reject or handle empty email appropriately
    # Currently this might succeed, but it's worth testing the behavior
    assert response.status_code in [200, 400]


def test_signup_case_sensitive_activity_names(client, reset_activities):
    """
    Test that activity names are case-sensitive
    """
    email = "alice@mergington.edu"
    
    # Lowercase version should not match
    response = client.post(f"/activities/chess club/signup?email={email}")
    assert response.status_code == 404


def test_signup_response_structure(client, reset_activities):
    """
    Test that successful signup returns correct response structure
    """
    email = "alice@mergington.edu"
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert isinstance(data["message"], str)
    assert email in data["message"]
    assert "Chess Club" in data["message"]
