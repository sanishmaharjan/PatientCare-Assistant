#!/bin/bash
# Control script for PatientCare Assistant servers

# Define color codes for better readability
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
RESET='\033[0m'

# Print banner
function print_banner {
    echo -e "${BLUE}${BOLD}"
    echo "┌───────────────────────────────────────────────────┐"
    echo "│        PatientCare Assistant Server Control       │"
    echo "└───────────────────────────────────────────────────┘"
    echo -e "${RESET}"
}

# Print status message with color
function print_status {
    local msg="$1"
    local color="$2"
    echo -e "${color}${msg}${RESET}"
}

# Activate the Python virtual environment
function activate_venv {
    if [ -d "venv_py3" ]; then
        source venv_py3/bin/activate
        print_status "✓ Python virtual environment activated" "$GREEN"
    else
        print_status "❌ Error: Virtual environment not found. Please run setup_python3.sh first." "$RED"
        exit 1
    fi
}

# Check required dependencies
function check_dependencies {
    if ! python -c "import psutil" &> /dev/null; then
        print_status "Installing required package: psutil..." "$YELLOW"
        if pip install psutil; then
            print_status "✓ psutil installed successfully" "$GREEN"
        else
            print_status "❌ Failed to install psutil. Please install it manually: pip install psutil" "$RED"
            exit 1
        fi
    fi
}

# Parse command-line arguments
ACTION=""
SERVERS="both"
VERBOSE=false

# Display usage information
function show_usage {
    echo -e "${BOLD}Usage:${RESET} $0 [--start|--stop|--restart|--status] [--api|--frontend] [--verbose]"
    echo ""
    echo -e "${BOLD}Options:${RESET}"
    echo "  --start     Start the servers"
    echo "  --stop      Stop the servers"
    echo "  --restart   Restart the servers"
    echo "  --status    Show server status"
    echo ""
    echo "  --api       Only affect the API server"
    echo "  --frontend  Only affect the Frontend server"
    echo "  --verbose   Show detailed output and debug information"
    echo ""
    echo -e "${YELLOW}If neither --api nor --frontend is specified, both servers are affected.${RESET}"
    echo ""
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --start)
            ACTION="start"
            shift
            ;;
        --stop)
            ACTION="stop"
            shift
            ;;
        --restart)
            ACTION="restart"
            shift
            ;;
        --status)
            ACTION="status"
            shift
            ;;
        --api)
            SERVERS="api"
            shift
            ;;
        --frontend)
            SERVERS="frontend"
            shift
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --help|-h)
            print_banner
            show_usage
            exit 0
            ;;
        *)
            print_status "❌ Error: Unknown option $1" "$RED"
            show_usage
            exit 1
            ;;
    esac
done

# Validate arguments
if [ -z "$ACTION" ]; then
    print_status "❌ Error: You must specify an action (--start, --stop, --restart, or --status)" "$RED"
    show_usage
    exit 1
fi

print_banner

# Activate virtual environment and check dependencies
activate_venv
check_dependencies

# Build the command arguments
CMD_ARGS="--$ACTION"
if [ "$SERVERS" == "api" ]; then
    CMD_ARGS="$CMD_ARGS --api"
    SERVER_DESC="API server"
elif [ "$SERVERS" == "frontend" ]; then
    CMD_ARGS="$CMD_ARGS --frontend"
    SERVER_DESC="Frontend server"
else
    SERVER_DESC="all servers"
fi

# Add verbose flag if needed
if [ "$VERBOSE" = true ]; then
    CMD_ARGS="$CMD_ARGS --verbose"
    print_status "Verbose mode enabled" "$BLUE"
fi

# Show what we're doing
case "$ACTION" in
    start)
        print_status "Starting ${SERVER_DESC}..." "$GREEN"
        ;;
    stop)
        print_status "Stopping ${SERVER_DESC}..." "$YELLOW"
        ;;
    restart)
        print_status "Restarting ${SERVER_DESC}..." "$YELLOW"
        ;;
    status)
        print_status "Checking status of ${SERVER_DESC}..." "$BLUE"
        ;;
esac

# Execute the server control command
if python src/server_control.py $CMD_ARGS; then
    # Command succeeded
    case "$ACTION" in
        start)
            print_status "✓ ${SERVER_DESC} started successfully" "$GREEN"
            ;;
        stop)
            print_status "✓ ${SERVER_DESC} stopped successfully" "$GREEN"
            ;;
        restart)
            print_status "✓ ${SERVER_DESC} restarted successfully" "$GREEN"
            ;;
        status)
            # Status already outputs its own messages
            ;;
    esac
    exit_code=0
else
    # Command failed
    exit_code=$?
    case "$ACTION" in
        start)
            print_status "❌ Failed to start ${SERVER_DESC}" "$RED"
            ;;
        stop)
            print_status "❌ Failed to stop ${SERVER_DESC}" "$RED"
            ;;
        restart)
            print_status "❌ Failed to restart ${SERVER_DESC}" "$RED"
            ;;
        status)
            print_status "❌ Failed to check status of ${SERVER_DESC}" "$RED"
            ;;
    esac
fi

# Deactivate the virtual environment
deactivate

# Return the exit code from the Python command
exit $exit_code
