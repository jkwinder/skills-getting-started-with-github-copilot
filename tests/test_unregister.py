"""Tests for DELETE /activities/{activity_name}/unregister endpoint using AAA pattern."""

import pytest


class TestUnregisterFromActivity:
    """Test suite for unregistering a student from an activity."""

    def test_successful_unregister_returns_200(self, client):
        """Test that successful unregister returns status code 200."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already registered

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200

    def test_successful_unregister_returns_message(self, client):
        """Test that successful unregister returns a success message."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        expected_message = f"Unregistered {email} from {activity_name}"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert "message" in data
        assert data["message"] == expected_message

    def test_participant_removed_from_activity(self, client):
        """Test that a participant is actually removed from the activity."""
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        # Verify by fetching activities
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email not in activities[activity_name]["participants"]

    def test_unregister_non_registered_participant_returns_400(self, client):
        """Test that unregistering a non-registered participant returns 400."""
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"  # Not registered

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400

    def test_unregister_non_registered_participant_returns_error_message(self, client):
        """Test that unregistering non-registered participant returns appropriate error."""
        # Arrange
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"
        expected_detail = "Student is not registered for this activity"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert "detail" in data
        assert data["detail"] == expected_detail

    def test_unregister_from_nonexistent_activity_returns_404(self, client):
        """Test that unregistering from a non-existent activity returns 404."""
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404

    def test_unregister_from_nonexistent_activity_returns_error_message(self, client):
        """Test that unregistering from non-existent activity returns appropriate error."""
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        expected_detail = "Activity not found"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        data = response.json()

        # Assert
        assert "detail" in data
        assert data["detail"] == expected_detail
