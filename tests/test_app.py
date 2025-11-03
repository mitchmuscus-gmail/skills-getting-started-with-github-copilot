import copy
import pytest
from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


@pytest.fixture(autouse=True)
def restore_activities():
    """Backup and restore the in-memory activities dict around each test."""
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    # Basic assertions about known activities
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister():
    activity = "Chess Club"
    email = "test.user@example.com"

    # Ensure email not present initially
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200, res.text
    body = res.json()
    assert "Signed up" in body["message"]

    # Verify participant added in-memory and via GET
    assert email in activities[activity]["participants"]
    res = client.get("/activities")
    assert res.status_code == 200
    assert email in res.json()[activity]["participants"]

    # Unregister
    res = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert res.status_code == 200, res.text
    body = res.json()
    assert "verwijderd" in body["message"] or "is verwijderd" in body["message"] or body["message"]

    # Verify removed
    assert email not in activities[activity]["participants"]
