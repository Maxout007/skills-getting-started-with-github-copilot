import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0

@pytest.mark.parametrize("activity,email", [
    ("Chess Club", "testuser@example.com"),
    ("Drama Club", "anotheruser@example.com")
])
def test_signup_and_unregister(activity, email):
    # Signup
    signup_url = f"/activities/{activity}/signup?email={email}"
    resp = client.post(signup_url)
    assert resp.status_code == 200
    # Check participant added
    resp2 = client.get("/activities")
    assert email in resp2.json()[activity]["participants"]
    # Unregister
    del_url = f"/activities/{activity}/participants/{email}"
    resp3 = client.delete(del_url)
    assert resp3.status_code == 200
    # Check participant removed
    resp4 = client.get("/activities")
    assert email not in resp4.json()[activity]["participants"]
