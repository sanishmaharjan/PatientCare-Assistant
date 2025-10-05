# PatientCare Assistant Server Management Guide

This document provides information on how to manage the PatientCare Assistant servers (API and Frontend).

## Using the Control Script

For command-line management, the `control.sh` script provides an easy way to manage the PatientCare Assistant servers.

### Basic Commands

```bash
# Start both servers
./control.sh --start

# Stop both servers
./control.sh --stop

# Restart both servers
./control.sh --restart

# Check server status
./control.sh --status
```

### Managing Specific Servers

```bash
# Only manage API server
./control.sh --start --api
./control.sh --stop --api
./control.sh --restart --api

# Only manage Frontend server
./control.sh --start --frontend
./control.sh --stop --frontend
./control.sh --restart --frontend
```

### Advanced Options

```bash
# Enable verbose output for debugging
./control.sh --start --verbose
./control.sh --status --verbose

# Get help about command usage
./control.sh --help
```

## Advanced Server Management

### Port Conflicts

The server control scripts automatically handle port conflicts:
- When starting the API server, it checks if port 8000 is already in use
- If the port is in use, it attempts to free it by killing the process
- Similarly for the frontend server and port 8501

### Process Detection

The server control scripts use robust process detection to find running servers:
- API server: Detects both direct Python invocations and uvicorn processes
- Frontend server: Detects Streamlit processes running the frontend app

### Common Issues and Solutions

#### API Server Not Starting

If the API server isn't starting properly:

```bash
# Check if port 8000 is in use
lsof -i :8000

# Manually kill any process using port 8000
kill -9 <PID>

# Start the API server with debug output
cd src/api && uvicorn app:app --host localhost --port 8000
```

#### Frontend Server Not Starting

If the frontend server isn't starting properly:

```bash
# Check if port 8501 is in use
lsof -i :8501

# Manually kill any process using port 8501
kill -9 <PID>

# Start the frontend server with debug output
cd src/frontend && streamlit run app.py
```

#### Restarting All Servers

For a clean restart of all services:

```bash
# Stop all servers
./control.sh --stop

# Wait a moment to ensure all processes are terminated
sleep 2

# Start all servers
./control.sh --start
```

## Troubleshooting

If you're experiencing issues with the servers, try the following steps:

1. **Check server status with verbose output**:
   ```bash
   ./control.sh --status --verbose
   ```

2. **Force restart the servers**:
   ```bash
   ./control.sh --restart --verbose
   ```

4. **Check for port conflicts**:
   ```bash
   lsof -i :8000   # Check if API port is in use
   lsof -i :8501   # Check if Frontend port is in use
   ```

5. **Check logs for error messages**:
   The control scripts now include enhanced error logging that will help identify issues.

6. **Check environment variables**:
   Ensure your OpenAI API key is correctly set in `src/.env`

7. **Server fails to start but no errors shown**:
   Run the start command with verbose logging:
   ```bash
   ./control.sh --start --verbose
   ```

8. **Server shows as running but is not responding**:
   The improved server status detection can now identify "zombie" processes or port conflicts.
   ```bash
   ./control.sh --status --verbose
   ```

## Manual Process Management

If the control scripts don't work, you can manually find and stop the processes:

```bash
# Find running API server (uvicorn)
ps aux | grep uvicorn

# Find running Frontend server (streamlit)
ps aux | grep streamlit

# Kill a process by PID
kill <PID>

# Kill a process forcefully
kill -9 <PID>

# Free up ports if they're in use
lsof -i :8000 | awk 'NR>1 {print $2}' | xargs -r kill -9
lsof -i :8501 | awk 'NR>1 {print $2}' | xargs -r kill -9
```

## System Requirements

The server management scripts require:

1. Python 3.x with virtual environment ('venv_py3')
2. The 'psutil' Python package (automatically installed by the scripts if needed)
3. Basic shell utilities (bash, lsof, grep, etc.)
4. Unix/Linux or macOS (Windows users should use WSL or Git Bash)
