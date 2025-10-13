# PatientCare Assistant - Troubleshooting Guide

This document outlines common issues and solutions for the PatientCare Assistant application.

## 🔌 API Connection Issues

If you encounter "Error connecting to API: [Errno 60] Operation timed out" or similar connection issues:

1. **Check API Server Status**: Ensure the API server is running
   ```bash
   curl http://localhost:8000/
   # Or use the control script
   ./scripts/control.sh --status
   ```

2. **Server Binding Issues**: The API server may be binding only to localhost. Verify the configuration:
   ```bash
   # Check if API is listening on the correct port
   lsof -i :8000
   ```

3. **Restart Services**: Use the control script for clean restart:
   ```bash
   ./scripts/control.sh --restart
   # Or restart specific services
   ./scripts/control.sh --restart --api
   ./scripts/control.sh --restart --frontend
   ```

4. **Check Dependencies**: Ensure all required packages are installed:
   ```bash
   source venv_py3/bin/activate
   pip install -r requirements.txt
   ```

5. **Manual API Start**: If the control script fails, you can start the API manually:
   ```bash
   cd src/api
   source ../../venv_py3/bin/activate
   python app.py
   ```

## 🎉 Recent Fixes and Updates

### API Service Startup Issue (RESOLVED)
**Date Fixed**: October 10, 2025
**Issue**: `./scripts/control.sh --start --api` was failing to start the API service due to import path issues in `src/api/app.py`
**Resolution**: Fixed the Python import path in the modular API startup script. The API now starts correctly via both:
- Control script: `./scripts/control.sh --start --api`
- Direct execution: `cd src/api && python app.py`

**Verification**: Test that the API is working:
```bash
curl http://localhost:8000/docs
curl -X POST "http://localhost:8000/summary" -H "Content-Type: application/json" -d '{"patient_id": "PATIENT-12346"}'
```

## 🔧 Known Issues and Fixes

### API Service Import Path Issue (Fixed)
**Problem**: The API fails to start with `ModuleNotFoundError: No module named 'api'`
**Solution**: This has been fixed in the modular API version. The import paths in `src/api/app.py` have been corrected.

### Server Control Process Detection
**Problem**: The control script may not correctly detect running API processes
**Workaround**: The API will still start and function correctly even if the status detection is not perfect. You can verify the API is running by testing: `curl http://localhost:8000/`

## 📄 Document Processing Issues

Common document processing problems and solutions:

1. **ChromaDB Database Conflicts**: If you see database lock errors:
   ```bash
   # Stop all processes and restart
   ./scripts/control.sh --stop
   ./scripts/control.sh --start
   ```

2. **Missing Document Dependencies**: For PDF processing issues:
   ```bash
   pip install pypdf docx2txt
   ```

3. **Large Document Processing**: For memory issues with large documents:
   - Documents are automatically chunked to prevent memory issues
   - Increase chunk size if needed in `src/config.py`
   - Use the clean processing script: `./scripts/run_processing.sh`

4. **Patient ID Extraction Failures**: If patient IDs are not being detected:
   - Check that documents contain valid patient ID patterns (PATIENT-XXXXX)
   - Review the extraction logic in `src/ingestion/patient_id_extraction.py`

5. **Vector Database Collection Issues**: If you see "Collection does not exist" errors:
   ```bash
   # Clear and rebuild the vector database
   rm -rf data/processed/vector_db
   ./scripts/run_processing.sh
   ```

## 🚀 Quick Resolution Commands

### Complete System Reset
```bash
# Stop all services
./scripts/control.sh --stop

# Clear and rebuild vector database (if needed)
rm -rf data/processed/vector_db
./scripts/run_processing.sh

# Clean restart with document reprocessing
./scripts/run_all.sh
```

### Minimal Startup (No warnings)
```bash
# Process documents cleanly
./scripts/run_processing.sh

# Start services individually
./scripts/control.sh --start --api
./scripts/control.sh --start --frontend

# Or start manually if control script has issues
cd src/api && source ../../venv_py3/bin/activate && python app.py &
source venv_py3/bin/activate && streamlit run src/frontend/app.py --server.port 8501 &
```

### Quick Diagnostic Commands
```bash
# Check if services are responding
curl http://localhost:8000/
curl http://localhost:8501/

# Test API functionality
curl -X POST "http://localhost:8000/summary" \
  -H "Content-Type: application/json" \
  -d '{"patient_id": "PATIENT-12346"}'

# Check process status
./scripts/control.sh --status --verbose

# View recent logs
tail -f logs/api.log
```

## 🔍 Advanced Troubleshooting

### Environment Issues
```bash
# Reset Python environment
rm -rf venv_py3
./scripts/setup_python3.sh

# Check Python version (3.8+ required, 3.13+ recommended)
python3 --version

# Verify dependencies
source venv_py3/bin/activate && pip list | grep -E "(fastapi|streamlit|langchain)"
```

### Data Directory Issues
```bash
# Check data directory structure
ls -la data/
ls -la data/raw/
ls -la data/processed/

# Reset data directories
mkdir -p data/{raw,processed,sample-data}
chmod -R 755 data/
```

### Port Conflicts
```bash
# Check what's using ports 8000 and 8501
lsof -i :8000
lsof -i :8501

# Kill processes using these ports
kill $(lsof -t -i:8000)
kill $(lsof -t -i:8501)
```

For additional troubleshooting and advanced configuration options, see the other documentation files in the `docs/` directory.
