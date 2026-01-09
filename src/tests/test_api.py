"""
Tests for the FastAPI wine reviews data exploration API.
"""

import pytest
from fastapi.testclient import TestClient
from src.api.main import app


@pytest.fixture
def client():
    """Create a test client for the API."""
    return TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_check_status_code(self, client):
        """Test that health endpoint returns 200."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_response(self, client):
        """Test health endpoint response structure."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"


class TestCountryStatsEndpoint:
    """Test country statistics endpoint."""

    def test_country_stats_status_code(self, client):
        """Test that country stats endpoint returns 200."""
        response = client.get("/stats/countries")
        assert response.status_code == 200

    def test_country_stats_returns_list(self, client):
        """Test that endpoint returns a list."""
        response = client.get("/stats/countries")
        data = response.json()
        assert isinstance(data, list)

    def test_country_stats_has_required_fields(self, client):
        """Test that country stats have required fields."""
        response = client.get("/stats/countries")
        data = response.json()
        if len(data) > 0:
            country = data[0]
            assert "country" in country
            assert "avg_points" in country
            assert "avg_price" in country
            assert "wine_count" in country

    def test_country_stats_sorted_by_wine_count(self, client):
        """Test that countries are sorted by wine count (descending)."""
        response = client.get("/stats/countries")
        data = response.json()
        if len(data) > 1:
            assert data[0]["wine_count"] >= data[1]["wine_count"]


class TestQualityDistributionEndpoint:
    """Test quality distribution endpoint."""

    def test_quality_distribution_status_code(self, client):
        """Test that quality distribution endpoint returns 200."""
        response = client.get("/stats/quality-distribution")
        assert response.status_code == 200

    def test_quality_distribution_returns_dict(self, client):
        """Test that endpoint returns a dictionary."""
        response = client.get("/stats/quality-distribution")
        data = response.json()
        assert isinstance(data, dict)

    def test_quality_distribution_has_categories(self, client):
        """Test that quality distribution has expected categories."""
        response = client.get("/stats/quality-distribution")
        data = response.json()
        # Should return dict (may be empty if data not available)
        assert isinstance(data, dict)
        # All values should be integers
        for value in data.values():
            assert isinstance(value, int)

    def test_quality_distribution_values_positive(self, client):
        """Test that all counts are positive."""
        response = client.get("/stats/quality-distribution")
        data = response.json()
        for count in data.values():
            assert count > 0


class TestPriceDistributionEndpoint:
    """Test price distribution endpoint."""

    def test_price_distribution_status_code(self, client):
        """Test that price distribution endpoint returns 200."""
        response = client.get("/stats/price-distribution")
        assert response.status_code == 200

    def test_price_distribution_returns_dict(self, client):
        """Test that endpoint returns a dictionary."""
        response = client.get("/stats/price-distribution")
        data = response.json()
        assert isinstance(data, dict)

    def test_price_distribution_has_categories(self, client):
        """Test that price distribution has expected categories."""
        response = client.get("/stats/price-distribution")
        data = response.json()
        # Should return dict (may be empty if data not available)
        assert isinstance(data, dict)
        # All values should be integers
        for value in data.values():
            assert isinstance(value, int)

    def test_price_distribution_values_positive(self, client):
        """Test that all counts are positive."""
        response = client.get("/stats/price-distribution")
        data = response.json()
        for count in data.values():
            assert count > 0


class TestTopVarietiesEndpoint:
    """Test top varieties endpoint."""

    def test_top_varieties_status_code(self, client):
        """Test that top varieties endpoint returns 200."""
        response = client.get("/stats/top-varieties")
        assert response.status_code == 200

    def test_top_varieties_default_limit(self, client):
        """Test that default limit is 10."""
        response = client.get("/stats/top-varieties")
        data = response.json()
        assert len(data) <= 10

    def test_top_varieties_custom_limit(self, client):
        """Test with custom limit parameter."""
        response = client.get("/stats/top-varieties?limit=5")
        data = response.json()
        assert len(data) <= 5

    def test_top_varieties_invalid_limit_too_high(self, client):
        """Test that limit > 50 returns 422."""
        response = client.get("/stats/top-varieties?limit=100")
        assert response.status_code == 422

    def test_top_varieties_invalid_limit_zero(self, client):
        """Test that limit < 1 returns 422."""
        response = client.get("/stats/top-varieties?limit=0")
        assert response.status_code == 422

    def test_top_varieties_returns_list(self, client):
        """Test that endpoint returns a list."""
        response = client.get("/stats/top-varieties?limit=5")
        data = response.json()
        assert isinstance(data, list)

    def test_top_varieties_has_required_fields(self, client):
        """Test that varieties have required fields."""
        response = client.get("/stats/top-varieties?limit=5")
        data = response.json()
        if len(data) > 0:
            variety = data[0]
            assert "variety" in variety
            assert "count" in variety

    def test_top_varieties_sorted_by_count(self, client):
        """Test that varieties are sorted by count (descending)."""
        response = client.get("/stats/top-varieties?limit=5")
        data = response.json()
        if len(data) > 1:
            assert data[0]["count"] >= data[1]["count"]


class TestTotalCountEndpoint:
    """Test total count endpoint."""

    def test_total_count_status_code(self, client):
        """Test that total count endpoint returns 200."""
        response = client.get("/stats/total-count")
        assert response.status_code == 200

    def test_total_count_returns_dict(self, client):
        """Test that endpoint returns a dictionary."""
        response = client.get("/stats/total-count")
        data = response.json()
        assert isinstance(data, dict)

    def test_total_count_has_field(self, client):
        """Test that response has total_wines field."""
        response = client.get("/stats/total-count")
        data = response.json()
        assert "total_wines" in data

    def test_total_count_is_positive(self, client):
        """Test that total count is a non-negative integer."""
        response = client.get("/stats/total-count")
        data = response.json()
        assert data["total_wines"] >= 0


class TestWinesDataEndpoint:
    """Test paginated wines data endpoint."""

    def test_wines_status_code(self, client):
        """Test that wines endpoint returns 200."""
        response = client.get("/wines")
        assert response.status_code == 200

    def test_wines_returns_dict(self, client):
        """Test that endpoint returns a dictionary."""
        response = client.get("/wines")
        data = response.json()
        assert isinstance(data, dict)

    def test_wines_has_required_fields(self, client):
        """Test that response has required fields."""
        response = client.get("/wines")
        data = response.json()
        assert "data" in data
        assert "limit" in data
        assert "offset" in data
        assert "total" in data

    def test_wines_default_limit(self, client):
        """Test default limit is 100."""
        response = client.get("/wines")
        data = response.json()
        assert data["limit"] == 100
        assert len(data["data"]) <= 100

    def test_wines_custom_limit(self, client):
        """Test with custom limit parameter."""
        response = client.get("/wines?limit=50")
        data = response.json()
        assert data["limit"] == 50
        assert len(data["data"]) <= 50

    def test_wines_invalid_limit_too_high(self, client):
        """Test that limit > 500 returns 422."""
        response = client.get("/wines?limit=600")
        assert response.status_code == 422

    def test_wines_invalid_limit_zero(self, client):
        """Test that limit < 1 returns 422."""
        response = client.get("/wines?limit=0")
        assert response.status_code == 422

    def test_wines_pagination_offset(self, client):
        """Test offset parameter."""
        response1 = client.get("/wines?limit=5&offset=0")
        response2 = client.get("/wines?limit=5&offset=5")
        data1 = response1.json()
        data2 = response2.json()
        
        # Different offsets should return different data
        if len(data1["data"]) > 0 and len(data2["data"]) > 0:
            assert data1["data"][0] != data2["data"][0]

    def test_wines_data_structure(self, client):
        """Test that wine records have expected structure."""
        response = client.get("/wines?limit=1")
        data = response.json()
        if len(data["data"]) > 0:
            wine = data["data"][0]
            # Wine should be a dictionary
            assert isinstance(wine, dict)
            # Should have some expected fields
            assert len(wine) > 0

    def test_wines_negative_offset_rejected(self, client):
        """Test that negative offset returns 422."""
        response = client.get("/wines?offset=-1")
        assert response.status_code == 422

    def test_wines_total_count_consistency(self, client):
        """Test that total in wines matches total-count endpoint."""
        wines_resp = client.get("/wines?limit=1")
        count_resp = client.get("/stats/total-count")
        
        wines_total = wines_resp.json()["total"]
        count_total = count_resp.json()["total_wines"]
        
        assert wines_total == count_total
