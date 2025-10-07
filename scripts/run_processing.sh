#!/bin/bash
#
# Simple Document Processing Script for PatientCare Assistant
#

# Set environment variables
export ANONYMIZED_TELEMETRY=False
export CHROMA_TELEMETRY=False
export PYTHONWARNINGS="ignore::DeprecationWarning"

echo "💼 PatientCare Assistant - Document Processor"
echo "--------------------------------------------"
echo "🔍 Processing documents..."

# Change to project directory
cd "$(dirname "$0")"

# Activate virtual environment if available
if [ -d "venv_py3" ]; then
  source venv_py3/bin/activate
fi

# Process documents - filter out telemetry and duplicate ID warnings
python3 -m src.main --process 2>&1 | grep -v "Failed to send telemetry event" | grep -v "Add of existing embedding ID"

# Check if the command succeeded
if [ ${PIPESTATUS[0]} -eq 0 ]; then
  echo "✅ Document processing completed successfully!"
else
  echo "❌ Document processing failed!"
  exit 1
fi
