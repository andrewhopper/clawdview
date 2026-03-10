"""Tests for health endpoints."""

from fastapi.testclient import TestClient


class TestHealthEndpoints:
    """Tests for health check endpoints."""

    def test_health_check(self, client: TestClient) -> None:
        """Test health endpoint returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data

    def test_readiness_check(self, client: TestClient) -> None:
        """Test readiness endpoint."""
        response = client.get("/ready")
        assert response.status_code == 200
        assert response.json()["ready"] is True
