#!/bin/bash

# Change to the project root directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run the tests
echo "Running tests..."
python -m pytest tests/

# Print test coverage
echo "Generating test coverage report..."
python -m pytest --cov=src tests/

# Return to the original directory
cd - > /dev/null
