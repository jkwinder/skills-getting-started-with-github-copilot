"""Tests for GET /activities endpoint using AAA pattern."""


class TestGetActivities:
    """Test suite for retrieving all activities."""

    def test_get_all_activities_returns_200(self, client):
        """Test that GET /activities returns status code 200."""
        # Arrange
        expected_status = 200

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == expected_status

    def test_get_all_activities_returns_dict(self, client):
        """Test that GET /activities returns a dictionary of activities."""
        # Arrange
        expected_type = dict

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert isinstance(data, expected_type)

    def test_get_all_activities_contains_expected_fields(self, client):
        """Test that each activity has required fields."""
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data, dict)
            assert required_fields.issubset(activity_data.keys())

    def test_get_all_activities_participants_is_list(self, client):
        """Test that participants field is a list."""
        # Arrange
        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_data["participants"], list)

    def test_get_activities_returns_content(self, client):
        """Test that GET /activities returns non-empty activities."""
        # Arrange
        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert len(activities) > 0
