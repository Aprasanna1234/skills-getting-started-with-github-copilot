"""
Tests for the GET / redirect endpoint
"""

import pytest


def test_root_endpoint_redirects_to_static(client, reset_activities):
    """
    Test that GET / redirects to /static/index.html
    """
    response = client.get("/", follow_redirects=False)
    
    assert response.status_code == 307  # 307 Temporary Redirect
    assert response.headers["location"] == "/static/index.html"


def test_root_endpoint_redirect_follows(client, reset_activities):
    """
    Test that following the redirect from / leads to the static index page
    """
    response = client.get("/", follow_redirects=True)
    
    # Should get the HTML content from index.html
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
