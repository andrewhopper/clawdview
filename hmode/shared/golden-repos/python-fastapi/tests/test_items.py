"""Tests for items router."""

from fastapi.testclient import TestClient


class TestItemsRouter:
    """Tests for items CRUD operations."""

    def test_create_item(self, client: TestClient) -> None:
        """Test creating an item."""
        response = client.post(
            "/api/v1/items",
            json={"name": "Test Item", "description": "A test item"},
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Item"
        assert "id" in data

    def test_list_items(self, client: TestClient) -> None:
        """Test listing items."""
        response = client.get("/api/v1/items")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "total" in data

    def test_get_item_not_found(self, client: TestClient) -> None:
        """Test getting non-existent item."""
        response = client.get("/api/v1/items/nonexistent")
        assert response.status_code == 404
