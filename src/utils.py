"""
The utils module contains utility functions for the ShutdownX CLI tool.
"""

import re
from datetime import datetime, timedelta

def validate_time_format(input_time):
    """Validates the time format (HH:MM or HH:MM AM/PM)."""
    time_regex = r"^(?:[01]?\d|2[0-3]):[0-5]\d(?:\s?(AM|PM))?$"
    if not re.match(time_regex, input_time, re.IGNORECASE):
        raise ValueError((
            "Invalid time format."
            "Use [i sea_green3]HH:MM[/i sea_green3] "
            "or [i light_goldenrod3]HH:MM AM/PM[/i light_goldenrod3]."
        ))

def calculate_seconds_until(target_time):
    """Calculates seconds from now until the target time."""
    current_time = datetime.now()

    if "AM" in target_time.upper() or "PM" in target_time.upper():
        parsed_time = datetime.strptime(target_time, "%I:%M %p")
    else:
        parsed_time = datetime.strptime(target_time, "%H:%M")

    shutdown_datetime = current_time.replace(
        hour=parsed_time.hour, minute=parsed_time.minute, second=0, microsecond=0
    )
    if shutdown_datetime < current_time:
        shutdown_datetime += timedelta(days=1)  # Schedule for the next day

    return int((shutdown_datetime - current_time).total_seconds()), shutdown_datetime

def calculate_seconds_from_now(duration):
    """
    Calculates seconds for a given duration string.
    Supports formats like:
    - '2h 30m', '1 hours 3 minutes', '15 seconds'
    - Compact formats: '2h30m', '1h15s'
    - Time-based formats: 'HH:MM' or 'HH:MM:SS' (e.g., '01:30', '00:03:10')
    """
    # Match for verbose or compact duration components like '2h 30m', '1 hours', etc.
    component_regex = r"(?:(\d+)\s*(hours?|h))?\s*(?:(\d+)\s*(minutes?|m))?\s*(?:(\d+)\s*(seconds?|s))?$"
    match = re.fullmatch(component_regex, duration.strip(), re.IGNORECASE)

    if match:
        # Extract components
        hours = int(match.group(1)) if match.group(1) else 0
        minutes = int(match.group(3)) if match.group(3) else 0
        seconds = int(match.group(5)) if match.group(5) else 0

        # Calculate total seconds
        total_seconds = hours * 3600 + minutes * 60 + seconds
        if total_seconds == 0:
            raise ValueError("Invalid duration format. [i]Duration cannot be [bold red]ZERO[/bold red].[/i]")

        return total_seconds

    # If the compact format fails, check for HH:MM:SS or HH:MM
    time_regex = r"^(\d{1,2}):(\d{2})(?::(\d{2}))?$"
    time_match = re.fullmatch(time_regex, duration.strip())

    if time_match:
        # Parse HH:MM:SS or HH:MM
        hours = int(time_match.group(1))
        minutes = int(time_match.group(2))
        seconds = int(time_match.group(3)) if time_match.group(3) else 0
        return hours * 3600 + minutes * 60 + seconds

    # If none of the formats match, raise an error
    raise ValueError(
        (
            "Invalid duration format."
            "Use formats like [i steel_blue3]2h 30m[/i steel_blue3], "
            "[i sea_green3]1 hours 3 minutes[/i sea_green3], "
            "[i hot_pink3]15s[/i hot_pink3], "
            "[i light_goldenrod3]01:30[/i light_goldenrod3], "
            "or [i plum3]00:03:10[/i plum3]."
        )
    )
