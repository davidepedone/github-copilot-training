"""Unit tests for main.py utility functions."""
import pytest
from app.main import fetch_all_tasks, generate_productivity_report, MOCK_TASKS
from app.models import DeveloperTask, ProductivityReport, TaskStatus


@pytest.mark.asyncio
async def test_fetch_all_tasks_returns_list_of_tasks() -> None:
    """Test that fetch_all_tasks returns a list of DeveloperTask instances."""
    tasks = await fetch_all_tasks()
    assert isinstance(tasks, list)
    assert len(tasks) == 3
    assert all(isinstance(task, DeveloperTask) for task in tasks)


@pytest.mark.asyncio
async def test_fetch_all_tasks_returns_expected_data() -> None:
    """Test that fetch_all_tasks returns the correct mock data."""
    tasks = await fetch_all_tasks()
    assert tasks[0].title == "Refactor legacy service"
    assert tasks[1].title == "Implement new user auth flow"
    assert tasks[2].title == "Write unit tests for checkout"


@pytest.mark.asyncio
async def test_generate_productivity_report_returns_productivity_report() -> None:
    """Test that generate_productivity_report returns a ProductivityReport instance."""
    report = await generate_productivity_report()
    assert isinstance(report, ProductivityReport)


@pytest.mark.asyncio
async def test_generate_productivity_report_calculates_correct_metrics() -> None:
    """Test that generate_productivity_report calculates metrics correctly."""
    report = await generate_productivity_report()
    assert report.total_tasks == 3
    assert report.completed_tasks == 1
    assert report.total_hours_spent == 23.5
    assert report.completion_rate == 0.33


@pytest.mark.asyncio
async def test_generate_productivity_report_handles_zero_tasks() -> None:
    """Test that generate_productivity_report handles empty task list gracefully."""
    # Temporarily clear tasks
    original_tasks = MOCK_TASKS.copy()
    MOCK_TASKS.clear()
    
    try:
        report = await generate_productivity_report()
        assert report.total_tasks == 0
        assert report.completed_tasks == 0
        assert report.total_hours_spent == 0.0
        assert report.completion_rate == 0.0
    finally:
        # Restore original tasks
        MOCK_TASKS.update(original_tasks)