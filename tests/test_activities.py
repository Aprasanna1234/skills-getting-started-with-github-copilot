"""
Tests for the GET /activities endpoint
"""

import pytest


def test_get_activities_returns_all_activities(client, reset_activities):
    """
    Test that GET /activities returns all available activities
    """
    # Arrange
    # Client and reset_activities fixture already set up
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_get_activities_returns_correct_activity_structure(client, reset_activities):
    """
    Test that each activity has the correct data structure and fields
    """
    # Arrange
    expected_fields = ["description", "schedule", "max_participants", "participants"]
    
    # Act
    response = client.get("/activities")
    data = response.json()
    chess_club = data["Chess Club"]
    
    # Assert
    assert response.status_code == 200
    for field in expected_fields:
        assert field in chess_club
    assert isinstance(chess_club["participants"], list)


def test_get_activities_includes_initial_participants(client, reset_activities):
    """
    Test that activities include their initial participants
    """
    # Arrange
    expected_participants = {
        "Chess Club": ["michael@mergington.edu", "daniel@mergington.edu"],
        "Programming Class": ["emma@mergington.edu", "sophia@mergington.edu"],
        "Gym Class": ["john@mergington.edu", "olivia@mergington.edu"]
    }
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity, participants in expected_participants.items():
        for participant in participants:
            assert participant in data[activity]["participants"]


def test_get_activities_returns_correct_max_participants(client, reset_activities):
    """
    Test that activities return correct max_participants capacity
    """
    # Arrange
    expected_capacities = {
        "Chess Club": 12,
        "Programming Class": 20,
        "Gym Class": 30
    }
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    for activity, capacity in expected_capacities.items():
        assert data[activity]["max_participants"] == capacity
