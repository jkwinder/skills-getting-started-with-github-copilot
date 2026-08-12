"""Tests for POST /activities/{activity_name}/signup endpoint using AAA pattern."""

import pytest


class TestSignupForActivity:
    """Test suite for signing up a student for an activity."""

    def test_successful_signup_returns_200(self, client):
        """Test that successful signup returns status code 200."""
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200

    def test_successful_signup_returns_message(self, client):
        """Test that successful signup returns a success message."""
        # Arrange
        activity_name = "Chess Club"
        email = "alice@mergington.edu"
        expected_message = f"Signed up {email} for {activity_name}"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert "message" in data
        assert data["message"] == expected_message

    def test_duplicate_signup_returns_400(self, client):
        """Test that signing up the same email twice returns 400."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400

    def test_duplicate_signup_returns_error_message(self, client):
        """Test that duplicate signup returns appropriate error message."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already in Chess Club
        expected_detail = "Student already signed up for this activity"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert "detail" in data
        assert data["detail"] == expected_detail

    def test_activity_not_found_returns_404(self, client):
        """Test that signing up for a non-existent activity returns 404."""
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404

    def test_activity_not_found_returns_error_message(self, client):
        """Test that non-existent activity returns appropriate error message."""
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        expected_detail = "Activity not found"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert "detail" in data
        assert data["detail"] == expected_detail

    def test_new_participant_added_to_activity(self, client):
        """Test that a new participant is actually added to the activity."""
        # Arrange
        activity_name = "Programming Class"
        email = "bob@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        # Verify by fetching activities
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]
