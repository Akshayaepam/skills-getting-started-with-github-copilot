import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: No setup needed for this test

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "Chess Club" in response.json()

def test_signup_for_activity():
    # Arrange
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert f"Signed up {email}" in response.json()["message"]

    # Cleanup: Remove the test user
    client.delete(f"/activities/{activity}/unregister?email={email}")

def test_signup_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "duplicateuser@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

    # Cleanup
    client.delete(f"/activities/{activity}/unregister?email={email}")

def test_unregister_participant():
    # Arrange
    activity = "Chess Club"
    email = "removeuser@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity}/unregister?email={email}")

    # Assert
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]

    # Try to remove again (should fail)
    response2 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert response2.status_code == 404
    assert "Participant not found" in response2.json()["detail"]
