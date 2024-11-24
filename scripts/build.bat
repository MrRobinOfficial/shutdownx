@echo off

REM Create the virtual environment if it doesn't exist
python -m venv .venv

REM Activate the virtual environment
CALL .venv\Scripts\activate.bat

REM Install the dependencies from requirements.txt
pip install -r requirements.txt

REM Run PyInstaller to create the .exe file with the required dependencies
pyinstaller --onefile --clean --name shutdownx --icon=img\icon.ico --add-data "requirements.txt:." --copy-metadata readchar src\main.py

REM Deactivate the virtual environment after building the exe
deactivate

REM Exit the script
exit
