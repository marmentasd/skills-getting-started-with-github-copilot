from fastapi.testclient import TestClient

from src.app import activities, app


client = TestClient(app)


def test_signup_participant_adds_email_to_activity():
    activity_name = "Chess Club"
    email = "student.signup@mergington.edu"

    activities[activity_name]["participants"] = [
        participant
        for participant in activities[activity_name]["participants"]
        if participant != email
    ]

    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    assert response.status_code == 200
    assert email in activities[activity_name]["participants"]


def test_duplicate_signup_returns_400():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_unknown_activity_returns_404():
    response = client.post("/activities/Unknown Activity/signup?email=test@example.com")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_list_activities_returns_activity_data():
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert "participants" in payload["Chess Club"]


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"

    activities[activity_name]["participants"].append(email)

    response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )

    assert response.status_code == 200
    assert email not in activities[activity_name]["participants"]


def test_unregister_missing_participant_returns_404():
    activity_name = "Chess Club"
    email = "missing.student@mergington.edu"

    response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not registered for this activity"
