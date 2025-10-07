# PatientCare Assistant - Launcher Scripts

This document describes the various launcher scripts available for running the PatientCare Assistant application.

## Available Scripts

### 1. `scripts/run_all.sh` - All-in-One Launcher (Recommended)

This script provides a complete solution for running the PatientCare Assistant application:
- Sets up the environment
- Processes documents
- Starts both API and frontend servers
- Provides colorized output with clear status indicators
- Suppresses unnecessary warnings

```bash
./scripts/run_all.sh
```

### 2. `scripts/run_processing.sh` - Document Processing

This script focuses solely on document processing:
- Sets up the environment
- Processes documents with clean output (no warnings)
- Provides clear success/failure indication

```bash
./scripts/run_processing.sh
```

### 3. `scripts/run_servers.sh` - Server Launcher

This script starts the API and frontend servers:
- Checks port availability
- Launches API and frontend servers
- Provides clear success/failure indication

```bash
./scripts/run_servers.sh
```

### 4. `scripts/control.sh` - Server Control

Legacy script for managing servers:
- Allows starting, stopping, and restarting servers
- Provides server status information

```bash
./scripts/control.sh --start    # Start both servers
./scripts/control.sh --stop     # Stop both servers
./scripts/control.sh --restart  # Restart both servers
./scripts/control.sh --status   # Check server status
```

### 5. Direct Python Commands

For more granular control, you can use direct Python commands:

```bash
# Process documents
python -m src.main --process

# Start API server only
python -m src.main --api

# Start frontend server only
python -m src.main --frontend

# Run everything (setup, processing, API, frontend)
python -m src.main --all
```

## Troubleshooting

If you encounter any issues with these scripts:

1. Make sure you've activated the virtual environment:
```bash
source venv_py3/bin/activate
```

2. Check for port conflicts (8000 for API, 8501 for frontend)

3. See the [troubleshooting guide](troubleshooting.md) for more details
