#!/bin/bash

# Create the virtual environment if it doesn't exist
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the dependencies from requirements.txt
pip install -r requirements.txt

# Install PyInstaller if not already installed
pip install pyinstaller

# Run PyInstaller to create the .exe file with the required dependencies
pyinstaller --onefile --name shutdownx --add-data "requirements.txt:." --copy-metadata readchar main.py

# Deactivate the virtual environment after building the exe
deactivate
