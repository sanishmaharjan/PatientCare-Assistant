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

# Clean restart with document reprocessing
./scripts/run_all.sh
```

### Minimal Startup (No warnings)
```bash
# Process documents cleanly
./scripts/run_processing.sh

# Start servers manually
python src/main.py --api &
python src/main.py --frontend &
```

For additional troubleshooting and advanced configuration options, see the other documentation files in the `docs/` directory.
