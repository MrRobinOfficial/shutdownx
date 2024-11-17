"""
The main module for the ShutdownX CLI tool.
"""

import platform
import subprocess
import argparse
import traceback
from datetime import datetime, timedelta
import inquirer
from rich.console import Console
from utils import calculate_seconds_from_now, validate_time_format, calculate_seconds_until

console = Console()

def handle_shutdown(seconds_time, preview_time):
    """Executes the shutdown command with a confirmation step."""
    try:
        console.print(f"[bold yellow] The computer will shut down at: {preview_time} [/bold yellow]")
        confirm = inquirer.confirm(
            message=f"Are you sure you want to schedule a shutdown for {preview_time}?", 
            default=False
        )
        if confirm:
            result = subprocess.run(["shutdown", "-s", "-f", "-t",
                str(seconds_time)],
                capture_output=True,
                text=True,
                check=False
            )

            if result.stderr:
                console.print(f"[bold red]Error:[/bold red] {result.stderr}")
            else:
                console.print("[bold green]Shutdown has now been scheduled[/bold green]")
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
                        ("Specific Time \t - Schedule a shutdown at an exact time", "time"),
                        ("Duration Timer \t - Schedule a shutdown after a set duration", "duration"),
                        ("Remove Schedule \t - Remove the scheduled shutdown", "remove"),
                        ("Exit", "exit")
                    ]
                )
            ]
            mode_answer = inquirer.prompt(questions)["mode"]

            if mode_answer == "exit":
                console.print("[bold red]No shutdown has been scheduled.[/bold red]")
                break

            if mode_answer == "remove":
                result = subprocess.run(["shutdown", "-a"], capture_output=True, text=True, check=False)

                if result.stderr:
                    console.print(f"[bold red]Error:[/bold red] {result.stderr}")
                    continue

                console.print("[bold green]Shutdown has been removed.[/bold green]")
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
                        shutdown_seconds, shutdown_datetime_calc = calculate_seconds_until(shutdown_time)
                        handle_shutdown(shutdown_seconds, shutdown_datetime_calc.strftime("%Y-%m-%d %H:%M:%S"))
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
                        shutdown_seconds = calculate_seconds_from_now(duration)
                        shutdown_datetime_calc = datetime.now() + timedelta(seconds=shutdown_seconds)
                        handle_shutdown(shutdown_seconds, shutdown_datetime_calc.strftime("%Y-%m-%d %H:%M:%S"))
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
            raise ValueError("This script is [b]ONLY[/b] supported on [i sea_green3]Windows[/i sea_green3].")

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
    except TypeError:
        pass
    except Exception as e:
        traceback.print_exc()
