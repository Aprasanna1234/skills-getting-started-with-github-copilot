"""
Tests for the GET / redirect endpoint
"""

import pytest


def test_root_endpoint_redirects_to_static(client, reset_activities):
    """
    Test that GET / redirects to /static/index.html
    """
    # Arrange
    expected_location = "/static/index.html"
    expected_status = 307  # 307 Temporary Redirect
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == expected_status
    assert response.headers["location"] == expected_location


def test_root_endpoint_redirect_follows(client, reset_activities):
    """
    Test that following the redirect from / leads to the static index page
    """
    # Arrange
    expected_content_type = "text/html"
    
    # Act
    response = client.get("/", follow_redirects=True)
    content_type = response.headers.get("content-type", "")
    
    # Assert
    assert response.status_code == 200
    assert expected_content_type in content_type
