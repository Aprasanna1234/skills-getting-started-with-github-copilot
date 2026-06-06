"""
Tests for the GET /activities endpoint
"""

import pytest


def test_get_activities_returns_all_activities(client, reset_activities):
    """
    Test that GET /activities returns all available activities
    """
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify all three activities are present
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_get_activities_returns_correct_activity_structure(client, reset_activities):
    """
    Test that each activity has the correct data structure and fields
    """
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    # Check Chess Club structure
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_get_activities_includes_initial_participants(client, reset_activities):
    """
    Test that activities include their initial participants
    """
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify initial participants are present
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in data["Chess Club"]["participants"]
    assert "emma@mergington.edu" in data["Programming Class"]["participants"]
    assert "sophia@mergington.edu" in data["Programming Class"]["participants"]
    assert "john@mergington.edu" in data["Gym Class"]["participants"]
    assert "olivia@mergington.edu" in data["Gym Class"]["participants"]


def test_get_activities_returns_correct_max_participants(client, reset_activities):
    """
    Test that activities return correct max_participants capacity
    """
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["Chess Club"]["max_participants"] == 12
    assert data["Programming Class"]["max_participants"] == 20
    assert data["Gym Class"]["max_participants"] == 30
