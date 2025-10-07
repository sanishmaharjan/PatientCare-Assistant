#!/bin/bash
#
# Document Processing Script for PatientCare Assistant
# This script handles document processing with proper environment setup,
# warning suppression, and error handling.
#

# Text colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
RESET='\033[0m'

# Directory for project
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${PROJECT_DIR}/data"
RAW_DATA_DIR="${DATA_DIR}/raw"
PROCESSED_DATA_DIR="${DATA_DIR}/processed"
VECTOR_DB_DIR="${PROCESSED_DATA_DIR}/vector_db"

# Function to print banner
print_banner() {
  echo
  echo -e "${BLUE}╔═════════════════════════════════════════════════╗${RESET}"
  echo -e "${BLUE}║${CYAN} PatientCare Assistant - Document Processor ${BLUE}      ║${RESET}"
  echo -e "${BLUE}╚═════════════════════════════════════════════════╝${RESET}"
  echo
}

# Function to print section header
print_section() {
  echo -e "${CYAN}▶ $1${RESET}"
}

# Function to check and create directories
check_directories() {
  print_section "Checking data directories..."
  
  # Create directories if they don't exist
  mkdir -p "${RAW_DATA_DIR}"
  mkdir -p "${PROCESSED_DATA_DIR}"
  mkdir -p "${VECTOR_DB_DIR}"
  
  echo -e "  ${GREEN}✓${RESET} Raw data directory: ${RAW_DATA_DIR}"
  echo -e "  ${GREEN}✓${RESET} Processed data directory: ${PROCESSED_DATA_DIR}"
  echo -e "  ${GREEN}✓${RESET} Vector database directory: ${VECTOR_DB_DIR}"
}

# Function to check if raw files exist
check_raw_files() {
  print_section "Checking for raw documents..."
  
  RAW_FILE_COUNT=$(find "${RAW_DATA_DIR}" -type f \( -name "*.pdf" -o -name "*.md" -o -name "*.txt" -o -name "*.docx" \) | wc -l | tr -d ' ')
  
  if [ "${RAW_FILE_COUNT}" -eq 0 ]; then
    echo -e "  ${YELLOW}⚠️  No documents found in raw data directory.${RESET}"
    echo -e "  Please add documents to: ${RAW_DATA_DIR}"
    return 1
  else
    echo -e "  ${GREEN}✓${RESET} Found ${RAW_FILE_COUNT} documents to process"
    return 0
  fi
}

# Function to activate virtual environment
activate_venv() {
  print_section "Setting up environment..."
  
  # Set environment variables to disable telemetry
  export ANONYMIZED_TELEMETRY=False
  export CHROMA_TELEMETRY=False
  export PYTHONWARNINGS="ignore::DeprecationWarning:langchain"
  
  # Activate virtual environment if available
  if [ -d "${PROJECT_DIR}/venv_py3" ]; then
    source "${PROJECT_DIR}/venv_py3/bin/activate"
    echo -e "  ${GREEN}✓${RESET} Virtual environment activated"
  else
    echo -e "  ${YELLOW}⚠️  Virtual environment not found${RESET}"
    echo -e "  Using system Python installation"
  fi
}

# Function to process documents
process_documents() {
  print_section "Processing documents..."
  
  # Run the command with warnings filtered
  (cd "${PROJECT_DIR}" && python -W ignore::DeprecationWarning src/main.py --process 2>&1) | \
    grep -v "Failed to send telemetry event" | \
    grep -v "Add of existing embedding ID"
  
  # Check exit status using PIPESTATUS to get the status of python command, not grep
  RESULT=${PIPESTATUS[0]}
  
  if [ $RESULT -eq 0 ]; then
    echo -e "\n${GREEN}✅ Document processing completed successfully!${RESET}"
    return 0
  else
    echo -e "\n${RED}❌ Document processing failed with exit code $RESULT${RESET}"
    return 1
  fi
}

# Main function
main() {
  print_banner
  check_directories
  check_raw_files || return 1
  activate_venv
  process_documents
  return $?
}

# Execute main function
main
exit $?
