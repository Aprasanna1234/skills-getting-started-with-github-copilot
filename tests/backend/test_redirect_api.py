"""
Backend tests for the root redirect endpoint.
"""

import pytest


def test_root_endpoint_redirects_to_static(client, reset_activities):
    # Arrange / Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_root_endpoint_redirect_follows(client, reset_activities):
    # Arrange / Act
    response = client.get("/", follow_redirects=True)

    # Assert
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
