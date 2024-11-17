@echo off

REM Create the virtual environment if it doesn't exist
python -m venv .venv

REM Activate the virtual environment
CALL .venv\Scripts\activate.bat

REM Install the dependencies from requirements.txt
pip install -r requirements\test.txt

REM Run the unit tests with coverage
coverage run -m pytest

REM Generate the coverage report
coverage report

REM Lint the code
pylint .\src

REM Deactivate the virtual environment after building the exe
deactivate

REM Exit the script
exit
