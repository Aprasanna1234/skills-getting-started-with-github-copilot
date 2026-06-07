"""
Integration and additional endpoint tests for the FastAPI application
"""

import pytest

pytest.skip("Backend tests are consolidated under tests/backend", allow_module_level=True)


def test_api_documentation_available(client):
    """
    Test that API documentation endpoints are available
    """
    # OpenAPI schema should be available
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "info" in data


def test_api_has_title_and_description(client):
    """
    Test that the API has proper title and description in documentation
    """
    response = client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    
    assert data["info"]["title"] == "Mergington High School API"
    assert "extracurricular activities" in data["info"]["description"]


def test_invalid_http_method_on_activities(client, reset_activities):
    """
    Test that invalid HTTP methods return appropriate errors
    """
    # DELETE is not supported on /activities
    response = client.delete("/activities")
    assert response.status_code == 405  # Method Not Allowed


def test_invalid_http_method_on_signup(client, reset_activities):
    """
    Test that GET method is not allowed on signup endpoint
    """
    response = client.get("/activities/Chess Club/signup?email=test@example.com")
    assert response.status_code == 405  # Method Not Allowed


def test_activities_endpoint_response_content_type(client, reset_activities):
    """
    Test that /activities endpoint returns JSON content-type
    """
    response = client.get("/activities")
    assert "application/json" in response.headers.get("content-type", "")


def test_signup_endpoint_response_content_type(client, reset_activities):
    """
    Test that /activities/{activity_name}/signup endpoint returns JSON
    """
    response = client.post("/activities/Chess Club/signup?email=test@example.com")
    assert "application/json" in response.headers.get("content-type", "")


def test_multiple_activities_consistency(client, reset_activities):
    """
    Test that activities maintain state correctly across multiple requests
    """
    email1 = "alice@mergington.edu"
    email2 = "bob@mergington.edu"
    
    # Sign up first student to Chess Club
    client.post(f"/activities/Chess Club/signup?email={email1}")
    
    # Sign up second student to Programming Class
    client.post(f"/activities/Programming Class/signup?email={email2}")
    
    # Verify both signups are reflected in activities
    response = client.get("/activities")
    data = response.json()
    
    assert email1 in data["Chess Club"]["participants"]
    assert email2 in data["Programming Class"]["participants"]
    
    # Verify student counts are correct
    assert len(data["Chess Club"]["participants"]) == 3  # 2 initial + 1 new
    assert len(data["Programming Class"]["participants"]) == 3  # 2 initial + 1 new
    assert len(data["Gym Class"]["participants"]) == 2  # unchanged


def test_activity_descriptions_are_preserved(client, reset_activities):
    """
    Test that activity descriptions remain unchanged after signups
    """
    # Get initial activities
    initial_response = client.get("/activities")
    initial_data = initial_response.json()
    
    # Sign up a student
    client.post("/activities/Chess Club/signup?email=alice@mergington.edu")
    
    # Get activities again
    updated_response = client.get("/activities")
    updated_data = updated_response.json()
    
    # Verify descriptions haven't changed
    assert initial_data["Chess Club"]["description"] == updated_data["Chess Club"]["description"]
    assert initial_data["Programming Class"]["description"] == updated_data["Programming Class"]["description"]
    assert initial_data["Gym Class"]["description"] == updated_data["Gym Class"]["description"]


def test_activity_schedule_is_preserved(client, reset_activities):
    """
    Test that activity schedules remain unchanged after signups
    """
    initial_response = client.get("/activities")
    initial_data = initial_response.json()
    
    client.post("/activities/Programming Class/signup?email=student@mergington.edu")
    
    updated_response = client.get("/activities")
    updated_data = updated_response.json()
    
    # Verify schedules haven't changed
    assert initial_data["Chess Club"]["schedule"] == updated_data["Chess Club"]["schedule"]
    assert initial_data["Programming Class"]["schedule"] == updated_data["Programming Class"]["schedule"]


def test_max_participants_never_changes(client, reset_activities):
    """
    Test that max_participants capacity never changes after signups
    """
    initial_response = client.get("/activities")
    initial_data = initial_response.json()
    
    # Sign up many students
    for i in range(5):
        client.post(f"/activities/Gym Class/signup?email=student{i}@mergington.edu")
    
    updated_response = client.get("/activities")
    updated_data = updated_response.json()
    
    # Verify max_participants hasn't changed
    assert initial_data["Gym Class"]["max_participants"] == updated_data["Gym Class"]["max_participants"]
    assert updated_data["Gym Class"]["max_participants"] == 30


def test_signup_with_hyphenated_email(client, reset_activities):
    """
    Test signup with email addresses containing hyphens
    """
    email = "student-test@mergington.edu"
    response = client.post(f"/activities/Chess Club/signup?email={email}")
    
    # Should succeed with valid email format
    assert response.status_code == 200
    
    # Verify it was added
    activities_response = client.get("/activities")
    data = activities_response.json()
    assert email in data["Chess Club"]["participants"]
