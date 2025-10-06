#!/bin/bash
# Test the document processing pipeline manually

# Set base directory
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_DIR="$BASE_DIR/data"
RAW_DIR="$DATA_DIR/raw"
PROCESSED_DIR="$DATA_DIR/data/processed"

# Create test document
echo "Creating test document..."
echo "
# Test Patient Record

## Patient Information
- Name: Test Patient
- DOB: 01/01/1980
- Medical Record Number: MRN-12345

## Current Medications
- Metformin 500mg twice daily
- Lisinopril 10mg once daily

## Allergies
- Penicillin (rash)
- Shellfish (anaphylaxis)

## Recent Vitals
- BP: 120/80
- Pulse: 72
- Temperature: 98.6°F
- Respiratory Rate: 16
- Weight: 70kg

## Medical History
- Type 2 Diabetes Mellitus (diagnosed 2018)
- Hypertension (diagnosed 2017)
- Hyperlipidemia (diagnosed 2019)
" > "$RAW_DIR/test_patient.md"

echo "Created test document at $RAW_DIR/test_patient.md"
echo "Testing document processing..."

# Activate virtual environment if it exists
if [ -f "$BASE_DIR/venv_py3/bin/activate" ]; then
    source "$BASE_DIR/venv_py3/bin/activate"
fi

# Process document using Python
python -c "
import os
import sys
sys.path.append('$BASE_DIR/src')
from ingestion.document_processor import DocumentIngestion
from embedding.embedding_generator import EmbeddingGenerator

base_dir = '$BASE_DIR'
raw_dir = os.path.join(base_dir, 'data', 'raw')
processed_dir = os.path.join(base_dir, 'data', 'processed')

print('Processing documents...')
ingestion = DocumentIngestion(raw_dir, processed_dir)
processed_files = ingestion.process_directory()
print(f'Processed {len(processed_files)} files:')
for file in processed_files:
    print(f'  - {os.path.basename(file)}')

print('\\nGenerating embeddings...')
embedding_generator = EmbeddingGenerator()
embedding_generator.process_all_documents(processed_dir)
print('Embedding generation complete')
"

echo "Testing complete. Check the data/processed directory for results."
