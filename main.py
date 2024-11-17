import re
import platform
import subprocess
import argparse
import inquirer
from rich.console import Console
from datetime import datetime, timedelta

console = Console()

def validate_time_format(input_time):
    """Validates the time format (HH:MM or HH:MM AM/PM)."""
    time_regex = r"^(?:[01]?\d|2[0-3]):[0-5]\d(?:\s?(AM|PM))?$"
    if not re.match(time_regex, input_time, re.IGNORECASE):
        raise ValueError("Invalid time format. Use [i sea_green3]HH:MM[/i sea_green3] or [i light_goldenrod3]HH:MM AM/PM[/i light_goldenrod3].")

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

import re

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
        "Invalid duration format. Use formats like [i steel_blue3]2h 30m[/i steel_blue3], [i sea_green3]1 hours 3 minutes[/i sea_green3], [i hot_pink3]15s[/i hot_pink3], [i light_goldenrod3]01:30[/i light_goldenrod3], or [i plum3]00:03:10[/i plum3]."
    )

def handle_shutdown(seconds, preview_time):
    """Executes the shutdown command with a confirmation step."""
    try:
        console.print(f"[bold yellow] The computer will shut down at: {preview_time} [/bold yellow]")
        confirm = inquirer.confirm(
            message=f"Are you sure you want to schedule a shutdown for {preview_time}?", 
            default=False
        )
        if confirm:
            subprocess.run(["shutdown", "-s", "-f", "-t", str(seconds)])
            console.print(f"[bold green]Shutdown has now been scheduled[/bold green]")
        else:
            console.print("[bold red]Shutdown canceled.[/bold red]")
    except KeyboardInterrupt:
        console.print("\n[bold red]Shutdown process aborted.[/bold red]")

def interactive_mode():
    """Handles the interactive mode with back navigation and tooltips."""
    while True:
        try:
            questions = [
                inquirer.List(
                    "mode",
                    message="How would you like to schedule the shutdown?",
                    choices=[
                        ("Specific Time - Schedule a shutdown at an exact time", "time"),
                        ("Duration Timer - Schedule a shutdown after a set duration", "duration"),
                        ("Exit", "exit")
                    ]
                )
            ]
            mode_answer = inquirer.prompt(questions)["mode"]

            if mode_answer == "exit":
                console.print("[bold red]No shutdown has been scheduled.[/bold red]")
                break

            if mode_answer == "time":
                while True:
                    time_question = inquirer.Text(
                        'time', 
                        message="Enter the shutdown time (e.g., 22:30 or 10:30 AM)"
                    )
                    shutdown_time = inquirer.prompt([time_question])["time"]
                    try:
                        validate_time_format(shutdown_time)
                        seconds, shutdown_datetime = calculate_seconds_until(shutdown_time)
                        handle_shutdown(seconds, shutdown_datetime.strftime("%Y-%m-%d %H:%M:%S"))
                        return
                    except ValueError as ve:
                        console.print(f"[bold red]Error:[/bold red] {ve}")
                        if not inquirer.confirm(message="Would you like to try again?", default=True):
                            break

            elif mode_answer == "duration":
                while True:
                    duration_question = inquirer.Text(
                        'duration', 
                        message="Enter the timer duration (e.g., 2h 30m, 2 hours 10 minutes, 15s or 01:30)"
                    )
                    duration = inquirer.prompt([duration_question])["duration"]
                    try:
                        seconds = calculate_seconds_from_now(duration)
                        shutdown_datetime = datetime.now() + timedelta(seconds=seconds)
                        handle_shutdown(seconds, shutdown_datetime.strftime("%Y-%m-%d %H:%M:%S"))
                        return
                    except ValueError as ve:
                        console.print(f"[bold red]Error:[/bold red] {ve}")
                        if not inquirer.confirm(message="Would you like to try again?", default=True):
                            break
        except KeyboardInterrupt:
            console.print("[bold red]No shutdown has been scheduled.[/bold red]")
            break

if __name__ == "__main__":
    try:
        if platform.system() != "Windows":
            raise Exception("This script is [b]ONLY[/b] supported on [i sea_green3]Windows[/i sea_green3].")

        # CLI Argument Parsing
        parser = argparse.ArgumentParser(description="Schedule a computer shutdown.")
        parser.add_argument(
            "--time", 
            type=str, 
            help="Specify shutdown time in 'HH:MM' or 'HH:MM AM/PM' format."
        )
        parser.add_argument(
            "--duration", 
            type=str, 
            help="Specify shutdown timer in '2h 30m', '2 hours' 10 minutes', '15s' or '01:30', etc."
        )
        args = parser.parse_args()

        if args.time and args.duration:
            raise ValueError("You cannot specify both --time and --duration. [i]Use one.[/i]")

        if args.time:
            validate_time_format(args.time)
            seconds, shutdown_datetime = calculate_seconds_until(args.time)
            handle_shutdown(seconds, shutdown_datetime.strftime("%Y-%m-%d %H:%M:%S"))

        elif args.duration:
            seconds = calculate_seconds_from_now(args.duration)
            shutdown_datetime = datetime.now() + timedelta(seconds=seconds)
            handle_shutdown(seconds, shutdown_datetime.strftime("%Y-%m-%d %H:%M:%S"))

        else:
            # Start Interactive Mode
            interactive_mode()

    except KeyboardInterrupt:
        console.print("\n[bold red]Script aborted by user.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
