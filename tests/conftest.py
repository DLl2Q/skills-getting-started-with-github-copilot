import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """FastAPI test client for making HTTP requests."""
    return TestClient(app)


@pytest.fixture
def fresh_activities(monkeypatch):
    """Reset activities to a known test state before each test."""
    test_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": []
        }
    }
    monkeypatch.setattr("src.app.activities", test_activities)