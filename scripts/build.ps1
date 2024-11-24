# Create the virtual environment if it doesn't exist
if (-Not (Test-Path ".\.venv")) {
    python -m venv .\.venv
}

# Activate the virtual environment
& .\.venv\Scripts\Activate.ps1

# Install the dependencies from requirements.txt
pip install -r requirements.txt

# Run PyInstaller to create the .exe file with the required dependencies
pyinstaller --onefile --clean --name shutdownx --icon=img\icon.ico --add-data "requirements.txt;." --copy-metadata readchar src\main.py

# Deactivate the virtual environment
deactivate

# Exit the script
exit
