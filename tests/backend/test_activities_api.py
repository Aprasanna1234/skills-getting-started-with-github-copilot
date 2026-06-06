def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data


def test_signup_flow(client, reset_activities):
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]
