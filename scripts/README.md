# PatientCare Assistant Scripts

This directory contains shell scripts for managing the PatientCare Assistant application. All scripts are designed to work on macOS and Linux systems.

## 🚀 Quick Start Scripts

### `run_all.sh` - Complete System Launcher ⭐ **Recommended**
The all-in-one script that sets up, processes documents, and starts the entire system.

```bash
./scripts/run_all.sh
```

**Features:**
- Sets up environment variables
- Processes documents with clean output
- Starts both API and frontend servers
- Provides colorized status indicators
- Suppresses unnecessary warnings

### `run_processing.sh` - Document Processing
Processes documents with clean output and minimal warnings.

```bash
./scripts/run_processing.sh
```

**Features:**
- Filters telemetry warnings
- Shows processing progress
- Returns clear success/failure status

### `run_servers.sh` - Server Management
Starts both API and frontend servers with port availability checks.

```bash
./scripts/run_servers.sh
```

**Features:**
- Checks port availability (8000, 8501)
- Starts API and frontend servers
- Provides server status feedback

## 🎛️ Control & Management Scripts

### `control.sh` - Advanced Server Control
Comprehensive server management with start, stop, restart, and status commands.

```bash
# Basic usage
./scripts/control.sh --start           # Start both servers
./scripts/control.sh --stop            # Stop both servers
./scripts/control.sh --restart         # Restart both servers
./scripts/control.sh --status          # Check server status

# Target specific servers
./scripts/control.sh --start --api     # Start only API server
./scripts/control.sh --stop --frontend # Stop only frontend server

# Advanced options
./scripts/control.sh --status --verbose # Detailed status information
```

### `setup_python3.sh` - Environment Setup
Initial setup script for creating Python virtual environment and installing dependencies.

```bash
./scripts/setup_python3.sh
```

**Features:**
- Creates Python virtual environment
- Installs all required dependencies
- Sets up OpenAI API key configuration

## 🧪 Testing & Development Scripts

### `run_tests.sh` - Test Runner
Runs the complete test suite with coverage reporting.

```bash
./scripts/run_tests.sh
```

### `test_document_pipeline.sh` - Pipeline Testing
Tests the complete document processing pipeline with sample data.

```bash
./scripts/test_document_pipeline.sh
```

## 📊 Legacy & Alternative Scripts

### `process-documents.sh` - Detailed Document Processing
Enhanced document processing with additional validation and checks.

```bash
./scripts/process-documents.sh
```

**Features:**
- Validates data directories
- Checks for available documents
- Shows detailed progress information
- Enhanced error handling

### `process_docs.sh` & `process_docs_clean.sh` - Basic Processing
Simple document processing scripts for basic use cases.

```bash
./scripts/process_docs.sh        # Basic processing
./scripts/process_docs_clean.sh  # Processing with clean output
```

### `run.sh` - Legacy Launcher
Legacy script for basic application startup.

```bash
./scripts/run.sh --all  # Start everything
```

## 📋 Script Dependencies

All scripts require:
- **Python 3.8+** (optimized for Python 3.13+)
- **Virtual environment** (`venv_py3/`) created by `setup_python3.sh`
- **OpenAI API key** configured in `src/.env`

## 🔧 Script Permissions

Ensure all scripts have execute permissions:

```bash
chmod +x scripts/*.sh
```

## 📚 Additional Documentation

For more detailed information, see:
- [Launcher Scripts Guide](../docs/launcher-scripts.md)
- [Server Management Guide](../docs/server-management.md)
- [Troubleshooting Guide](../docs/troubleshooting.md)
- [Processing Scripts Guide](../docs/processing-scripts.md)

## 🆘 Common Issues

### Port Conflicts
If you get port conflict errors:
```bash
./scripts/control.sh --stop  # Stop any running services
lsof -i :8000                # Check what's using port 8000
lsof -i :8501                # Check what's using port 8501
```

### Virtual Environment Issues
If scripts can't find the virtual environment:
```bash
./scripts/setup_python3.sh   # Recreate virtual environment
```

### Permission Errors
If you get permission denied errors:
```bash
chmod +x scripts/*.sh        # Make all scripts executable
```

## 🏃‍♂️ Recommended Workflow

1. **Initial Setup:**
   ```bash
   ./scripts/setup_python3.sh
   ```

2. **Daily Usage:**
   ```bash
   ./scripts/run_all.sh
   ```

3. **Development/Testing:**
   ```bash
   ./scripts/run_processing.sh    # Process new documents
   ./scripts/run_servers.sh       # Start servers only
   ./scripts/run_tests.sh         # Run tests
   ```

4. **Server Management:**
   ```bash
   ./scripts/control.sh --status  # Check status
   ./scripts/control.sh --restart # Restart if needed
   ```
