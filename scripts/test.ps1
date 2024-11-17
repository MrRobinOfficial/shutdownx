# Create the virtual environment if it doesn't exist
if (-Not (Test-Path ".\.venv")) {
    python -m venv .\.venv
}

# Activate the virtual environment
& .\.venv\Scripts\Activate.ps1

# Install the dependencies from requirements.txt
pip install -r .\requirements\test.txt

# Run the unit tests with coverage
coverage run -m pytest

# Generate the coverage report
coverage report

# Lint the code
pylint .\src

# Deactivate the virtual environment
deactivate

# Exit the script
exit
