"""Integration tests for main.py endpoints."""
import pytest
from httpx import AsyncClient
from app.models import DeveloperTask, TaskStatus


@pytest.mark.asyncio
@pytest.mark.integration
async def test_status_endpoint_returns_200(client: AsyncClient) -> None:
    """Test that the /status endpoint returns 200 status code."""
    response = await client.get("/status")
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.integration
async def test_status_endpoint_returns_ok_status(client: AsyncClient) -> None:
    """Test that the /status endpoint returns OK status."""
    response = await client.get("/status")
    assert response.json() == {"status": "ok"}


@pytest.mark.asyncio
@pytest.mark.integration
async def test_tasks_endpoint_returns_200(client: AsyncClient) -> None:
    """Test that the /tasks endpoint returns 200 status code."""
    response = await client.get("/tasks")
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.integration
async def test_tasks_endpoint_returns_list_of_tasks(client: AsyncClient) -> None:
    """Test that the /tasks endpoint returns a list of tasks."""
    response = await client.get("/tasks")
    tasks = response.json()
    assert isinstance(tasks, list)
    assert len(tasks) == 3
    assert all("task_id" in task and "title" in task and "status" in task for task in tasks)


@pytest.mark.asyncio
@pytest.mark.integration
async def test_report_endpoint_returns_200(client: AsyncClient) -> None:
    """Test that the /report endpoint returns 200 status code."""
    response = await client.get("/report")
    assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.integration
async def test_report_endpoint_returns_productivity_report(client: AsyncClient) -> None:
    """Test that the /report endpoint returns a valid productivity report."""
    response = await client.get("/report")
    report = response.json()
    assert "total_tasks" in report
    assert "completed_tasks" in report
    assert "total_hours_spent" in report
    assert "completion_rate" in report
    assert report["total_tasks"] == 3
    assert report["completed_tasks"] == 1


@pytest.mark.asyncio
@pytest.mark.integration
async def test_log_task_endpoint_creates_task(client: AsyncClient) -> None:
    """Test that the /log_task endpoint successfully creates a task."""
    new_task = {
        "task_id": 0,
        "title": "Test new endpoint",
        "status": "pending",
        "hours_spent": 2.5
    }
    response = await client.post("/log_task", json=new_task)
    assert response.status_code == 200
    result = response.json()
    assert "task_id" in result
    assert result["message"] is not None


@pytest.mark.asyncio
@pytest.mark.integration
async def test_log_task_endpoint_returns_dict(client: AsyncClient) -> None:
    """Test that the /log_task endpoint returns a dictionary."""
    new_task = {
        "task_id": 0,
        "title": "Another test task",
        "status": "in_progress",
        "hours_spent": 1.0
    }
    response = await client.post("/log_task", json=new_task)
    assert isinstance(response.json(), dict)
