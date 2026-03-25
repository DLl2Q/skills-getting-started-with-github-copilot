import pytest


def test_root_redirect(client):
    """Test that GET / redirects to static/index.html."""
    # Arrange
    # Act
    response = client.get("/", follow_redirects=False)
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_success(client, fresh_activities):
    """Test that GET /activities returns all activities."""
    # Arrange
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert data["Chess Club"]["participants"] == ["michael@mergington.edu"]
    assert data["Programming Class"]["participants"] == []


def test_signup_success(client, fresh_activities):
    """Test successful signup for an activity."""
    # Arrange
    # Act
    response = client.post("/activities/Programming%20Class/signup?email=test@example.com")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Signed up test@example.com for Programming Class" in data["message"]
    # Verify data updated
    get_response = client.get("/activities")
    activities = get_response.json()
    assert "test@example.com" in activities["Programming Class"]["participants"]


def test_signup_activity_not_found(client):
    """Test signup for non-existent activity returns 404."""
    # Arrange
    # Act
    response = client.post("/activities/Nonexistent/signup?email=test@example.com")
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_signup_already_registered(client, fresh_activities):
    """Test signup when student is already registered returns 400."""
    # Arrange
    # Act
    response = client.post("/activities/Chess%20Club/signup?email=michael@mergington.edu")
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student is already signed up for this activity"


def test_remove_success(client, fresh_activities):
    """Test successful removal of a participant."""
    # Arrange
    # Act
    response = client.delete("/activities/Chess%20Club/participants?email=michael@mergington.edu")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Removed michael@mergington.edu from Chess Club" in data["message"]
    # Verify data updated
    get_response = client.get("/activities")
    activities = get_response.json()
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_remove_activity_not_found(client):
    """Test removal from non-existent activity returns 404."""
    # Arrange
    # Act
    response = client.delete("/activities/Nonexistent/participants?email=test@example.com")
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"


def test_remove_participant_not_found(client, fresh_activities):
    """Test removal of non-existent participant returns 404."""
    # Arrange
    # Act
    response = client.delete("/activities/Chess%20Club/participants?email=nonexistent@example.com")
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Participant not found"