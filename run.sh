#!/bin/bash

# Change to the project root directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Display the PatientCare Assistant banner
echo "-------------------------------------"
echo "    PatientCare Assistant Startup    "
echo "-------------------------------------"
echo "Running with Python 3"
echo "-------------------------------------"

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed or not in PATH. Please run setup_python3.sh first."
    exit 1
fi

# Check for command line arguments
if [ "$1" == "--setup" ]; then
    echo "Setting up the environment..."
    python3 src/main.py --setup
elif [ "$1" == "--process" ]; then
    echo "Processing documents..."
    python3 src/main.py --process
elif [ "$1" == "--api" ]; then
    echo "Starting API server..."
    python3 src/main.py --api
elif [ "$1" == "--frontend" ]; then
    echo "Starting frontend server..."
    python3 src/main.py --frontend
else
    # Default: start everything
    echo "Starting PatientCare Assistant..."
    echo "API will be available at: http://localhost:8000"
    echo "Frontend will be available at: http://localhost:8501"
    echo "-------------------------------------"
    python3 src/main.py --all
fi

# Return to the original directory
cd - > /dev/null
