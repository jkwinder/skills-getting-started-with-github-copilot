import pytest
from fastapi.testclient import TestClient
from src.app import app
import src.app


@pytest.fixture
def test_activities():
    """Provides a fresh copy of test activities for each test."""
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        }
    }


@pytest.fixture
def client(test_activities, monkeypatch):
    """Provides a test client with fresh activities for each test."""
    # Replace the app module's activities with fresh test data for this test
    monkeypatch.setattr(src.app, "activities", test_activities)
    
    return TestClient(app)
