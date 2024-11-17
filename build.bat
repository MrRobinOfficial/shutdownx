@echo off

REM Create the virtual environment if it doesn't exist
python -m venv .venv

REM Activate the virtual environment
call .venv\Scripts\activate

REM Install the dependencies from requirements.txt
pip install -r requirements.txt

REM Install PyInstaller if not already installed
pip install pyinstaller

REM Run PyInstaller to create the .exe file with the required dependencies
pyinstaller --onefile --name shutdownx --add-data "requirements.txt:." --copy-metadata readchar main.py

REM Deactivate the virtual environment after building the exe
deactivate

REM Exit the script
exit
