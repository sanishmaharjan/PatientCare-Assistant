#!/bin/bash
#
# Run the PatientCare Assistant servers (API and frontend)
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
  echo -e "${BLUE}║${CYAN} PatientCare Assistant - Server Launcher ${BLUE}       ║${RESET}"
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
  
  # Set environment variables
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

# Function to check if port is in use
check_port() {
  local port=$1
  if lsof -i :${port} > /dev/null; then
    echo -e "  ${RED}✗${RESET} Port ${port} is already in use"
    return 1
  else
    echo -e "  ${GREEN}✓${RESET} Port ${port} is available"
    return 0
  fi
}

# Function to start API server
start_api() {
  print_section "Starting API server..."
  
  # Check if port is available
  check_port 8000 || return 1
  
  # Start API server in background
  (cd "${PROJECT_DIR}" && python3 -m src.main --api) &
  API_PID=$!
  
  # Wait for API to start
  sleep 2
  
  # Check if API server started successfully
  if ps -p $API_PID > /dev/null; then
    echo -e "  ${GREEN}✓${RESET} API server started at ${GREEN}http://localhost:8000${RESET}"
    return 0
  else
    echo -e "  ${RED}✗${RESET} Failed to start API server"
    return 1
  fi
}

# Function to start frontend server
start_frontend() {
  print_section "Starting frontend server..."
  
  # Check if port is available
  check_port 8501 || return 1
  
  # Start frontend server in background
  (cd "${PROJECT_DIR}" && python3 -m src.main --frontend) &
  FRONTEND_PID=$!
  
  # Wait for frontend to start
  sleep 2
  
  # Check if frontend server started successfully
  if ps -p $FRONTEND_PID > /dev/null; then
    echo -e "  ${GREEN}✓${RESET} Frontend server started at ${GREEN}http://localhost:8501${RESET}"
    return 0
  else
    echo -e "  ${RED}✗${RESET} Failed to start frontend server"
    return 1
  fi
}

# Main function
main() {
  print_banner
  activate_venv
  
  start_api
  API_SUCCESS=$?
  
  start_frontend
  FRONTEND_SUCCESS=$?
  
  if [ $API_SUCCESS -eq 0 ] && [ $FRONTEND_SUCCESS -eq 0 ]; then
    echo
    echo -e "${GREEN}PatientCare Assistant is now running!${RESET}"
    echo -e "API server:     ${GREEN}http://localhost:8000${RESET}"
    echo -e "Frontend:       ${GREEN}http://localhost:8501${RESET}"
    echo
    echo -e "Press ${CYAN}Ctrl+C${RESET} to stop all servers"
    echo
    
    # Keep the script running so servers stay alive
    wait
  else
    echo
    echo -e "${RED}Failed to start servers${RESET}"
    exit 1
  fi
}

# Execute main function
main
