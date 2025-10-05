#!/bin/bash

# Script to process documents while suppressing specific warnings
# This script will filter out known warnings that don't impact functionality

# Set up environment variables
export ANONYMIZED_TELEMETRY=False
export CHROMA_TELEMETRY=False
export PYTHONWARNINGS="ignore::DeprecationWarning"

# Change to project directory
cd "$(dirname "$0")"

# Activate virtual environment if available
if [ -d "venv_py3" ]; then
  source venv_py3/bin/activate
fi

# Run the document processing and filter out known warnings
echo "Starting document processing..."
python src/main.py --process 2>&1 | grep -v "Failed to send telemetry event" | grep -v "Add of existing embedding ID"

# Check exit status using PIPESTATUS to get the status of python command, not grep
RESULT=${PIPESTATUS[0]}

if [ $RESULT -eq 0 ]; then
  echo "✅ Document processing completed successfully!"
else
  echo "❌ Document processing failed with exit code $RESULT"
  exit 1
fi
