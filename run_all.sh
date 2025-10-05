#!/bin/bash
#
# PatientCare Assistant - All-in-one Launcher
# This script handles document processing and starts the servers
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

# Function to print banner
print_banner() {
  echo
  echo -e "${BLUE}╔═════════════════════════════════════════════════╗${RESET}"
  echo -e "${BLUE}║${CYAN} PatientCare Assistant - All-in-one Launcher ${BLUE}    ║${RESET}"
  echo -e "${BLUE}╚═════════════════════════════════════════════════╝${RESET}"
  echo
}

# Function to print section header
print_section() {
  echo -e "${CYAN}▶ $1${RESET}"
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
  (cd "${PROJECT_DIR}" && python3 -m src.main --process 2>&1) | \
    grep -v "Failed to send telemetry event" | \
    grep -v "Add of existing embedding ID" | \
    grep -v "LangChainDeprecationWarning"
  
  # Check exit status using PIPESTATUS to get the status of python command, not grep
  RESULT=${PIPESTATUS[0]}
  
  if [ $RESULT -eq 0 ]; then
    echo -e "  ${GREEN}✓${RESET} Document processing completed successfully!"
    return 0
  else
    echo -e "  ${RED}✗${RESET} Document processing failed with exit code $RESULT"
    return 1
  fi
}

# Function to check if port is in use
check_port() {
  local port=$1
  if lsof -i :${port} > /dev/null 2>&1; then
    echo -e "  ${RED}✗${RESET} Port ${port} is already in use"
    return 1
  else
    echo -e "  ${GREEN}✓${RESET} Port ${port} is available"
    return 0
  fi
}

# Function to start servers
start_servers() {
  print_section "Starting servers..."
  
  # Check if ports are available
  echo "Checking port availability..."
  check_port 8000 && API_PORT_OK=true || API_PORT_OK=false
  check_port 8501 && FRONTEND_PORT_OK=true || FRONTEND_PORT_OK=false
  
  if [ "$API_PORT_OK" = false ] || [ "$FRONTEND_PORT_OK" = false ]; then
    echo -e "  ${RED}✗${RESET} Port conflict detected. Please free up the required ports."
    return 1
  fi
  
  echo -e "  Starting API server..."
  # Start API server
  (cd "${PROJECT_DIR}" && python3 -m src.main --api) &
  API_PID=$!
  sleep 2
  
  if ! ps -p $API_PID > /dev/null 2>&1; then
    echo -e "  ${RED}✗${RESET} Failed to start API server"
    return 1
  fi
  
  echo -e "  Starting frontend server..."
  # Start frontend server
  (cd "${PROJECT_DIR}" && python3 -m src.main --frontend) &
  FRONTEND_PID=$!
  sleep 2
  
  if ! ps -p $FRONTEND_PID > /dev/null 2>&1; then
    echo -e "  ${RED}✗${RESET} Failed to start frontend server"
    # Kill API server since frontend failed
    kill $API_PID 2>/dev/null
    return 1
  fi
  
  echo -e "  ${GREEN}✓${RESET} API server started at ${GREEN}http://localhost:8000${RESET}"
  echo -e "  ${GREEN}✓${RESET} Frontend server started at ${GREEN}http://localhost:8501${RESET}"
  return 0
}

# Main function
main() {
  print_banner
  activate_venv
  
  # Process documents
  process_documents
  if [ $? -ne 0 ]; then
    echo -e "${RED}Aborting due to document processing failure${RESET}"
    exit 1
  fi
  
  # Start servers
  start_servers
  if [ $? -ne 0 ]; then
    echo -e "${RED}Aborting due to server startup failure${RESET}"
    exit 1
  fi
  
  echo
  echo -e "${GREEN}PatientCare Assistant is now running!${RESET}"
  echo -e "API server:     ${GREEN}http://localhost:8000${RESET}"
  echo -e "Frontend:       ${GREEN}http://localhost:8501${RESET}"
  echo
  echo -e "Press ${CYAN}Ctrl+C${RESET} to stop all servers"
  echo
  
  # Keep the script running so servers stay alive
  wait
}

# Execute main function
main
