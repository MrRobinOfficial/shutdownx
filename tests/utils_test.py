import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
from src.utils import validate_time_format, calculate_seconds_until, calculate_seconds_from_now

def test_validate_time_format():
    # Valid formats
    validate_time_format("12:30")
    validate_time_format("02:45 PM")
    validate_time_format("23:59")
    # Invalid formats
    with pytest.raises(ValueError):
        validate_time_format("25:00")  # Invalid hour
    with pytest.raises(ValueError):
        validate_time_format("12:60")  # Invalid minute
    with pytest.raises(ValueError):
        validate_time_format("12:30 PM AM")  # Invalid AM/PM
    with pytest.raises(ValueError):
        validate_time_format("random text")  # Invalid format

def test_calculate_seconds_until():
    # Mock current_time for consistency
    mock_current_time = datetime(2024, 11, 17, 14, 30)  # Set a fixed "current time"

    # Use patch to mock datetime methods in the 'utils' module
    with patch('src.utils.datetime') as mock_datetime:
        # Mock datetime methods
        mock_datetime.now.return_value = mock_current_time  # Mock datetime.now()
        mock_datetime.strptime = datetime.strptime

        # Test case 1: Target time later on the same day
        target_time = "03:00 PM"
        expected_seconds = 1800  # 30 minutes
        actual_seconds, _ = calculate_seconds_until(target_time)
        assert abs(actual_seconds - expected_seconds) < 1  # Allow slight differences due to execution time

        # Test case 2: Target time in the next day
        target_time = "14:00"
        expected_seconds = 84600  # 23 hours and 30 minutes
        actual_seconds, _ = calculate_seconds_until(target_time)
        assert abs(actual_seconds - expected_seconds) < 1

def test_calculate_seconds_from_now():
    # Verbose format
    assert calculate_seconds_from_now("1h 30m") == 5400
    assert calculate_seconds_from_now("2 hours 15 minutes 10 seconds") == 8110
    # Compact format
    assert calculate_seconds_from_now("1h30m") == 5400
    assert calculate_seconds_from_now("2h15s") == 7215
    # Time-based format
    assert calculate_seconds_from_now("01:30") == 5400
    assert calculate_seconds_from_now("00:03:10") == 190
    # Invalid formats
    with pytest.raises(ValueError):
        calculate_seconds_from_now("random text")
    with pytest.raises(ValueError):
        calculate_seconds_from_now("0h 0m 0s")  # Zero duration
