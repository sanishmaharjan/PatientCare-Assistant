# Document Processing Scripts

The `scripts/` directory contains several script options for processing documents in the PatientCare Assistant application.

## Available Scripts

1. **scripts/run_processing.sh** - The recommended simple script for document processing
   * Filters warning messages
   * Shows important processing information
   * Easy to use with clear output

2. **scripts/process-documents.sh** - More detailed processing script with additional checks
   * Validates data directories
   * Checks for available documents
   * Shows detailed progress information
   * Enhanced error handling

3. **scripts/process_docs.sh** and **scripts/process_docs_clean.sh** - Legacy scripts
   * Basic document processing functionality

## Usage

To process documents:

```bash
# Recommended approach - simple and clean output
./scripts/run_processing.sh

# For more detailed checks and information
./scripts/process-documents.sh
```

These scripts set up the proper environment variables and Python environment before running the document processing, ensuring compatibility across different systems.
