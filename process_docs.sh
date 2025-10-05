#!/bin/bash

# Script to process documents with proper environment setup
# This script will set up the environment variables correctly and run the document processing

# Set up environment variables
export ANONYMIZED_TELEMETRY=False
export CHROMA_TELEMETRY=False

# Change to project directory
cd "$(dirname "$0")"

# Activate virtual environment if available
if [ -d "venv_py3" ]; then
  source venv_py3/bin/activate
fi

# Run the document processing
echo "Starting document processing..."
python src/main.py --process

# Check exit status
if [ $? -eq 0 ]; then
  echo "✅ Document processing completed successfully!"
else
  echo "❌ Document processing failed!"
  exit 1
fi
