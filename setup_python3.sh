#!/bin/bash
# Setup script for Python 3 environment

# Check if Python 3 is installed
if command -v python3 &>/dev/null; then
    echo "Python 3 is installed"
    python3 --version
else
    echo "Python 3 is not installed. Please install Python 3 first."
    echo "On macOS with Homebrew: brew install python3"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# If OpenAI API key not set, prompt for it
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Please enter your OpenAI API key:"
    read api_key
    echo "export OPENAI_API_KEY=$api_key" >> venv/bin/activate
    export OPENAI_API_KEY=$api_key
fi

echo "Setup complete! You can now run the application with:"
echo "source venv/bin/activate && python src/main.py --all"
