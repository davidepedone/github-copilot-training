"""Shared test fixtures for the FastAPI application."""
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.fixture
async def client() -> AsyncClient:
    """Provides an async HTTP client for testing endpoints."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def app_fixture():
    """Provides the FastAPI app instance for testing."""
    return app
