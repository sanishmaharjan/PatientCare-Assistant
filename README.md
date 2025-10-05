# PatientCare Assistant

A generative AI-powered assistant for healthcare providers to quickly retrieve and analyze patient information from medical documents.

## Overview

PatientCare Assistant uses generative AI to help healthcare providers:
- Extract and organize information from patient documents
- Answer questions about patient medical history
- Generate summaries of patient data
- Identify potential issues or risks based on patient records
- Provide evidence-based insights from medical literature

## Features

- **Document Processing**: Automatically ingest, parse, and process PDF, DOCX, and text documents
- **Semantic Search**: Find relevant patient information using natural language queries
- **Medical Q&A**: Ask questions about patient records and get accurate answers
- **Patient Summaries**: Generate comprehensive summaries of patient information
- **Health Risk Analysis**: Identify potential health issues based on patient data
- **Interactive UI**: User-friendly interface designed for healthcare professionals

## Architecture

The application follows a modular architecture:

1. **Data Ingestion**: Process PDFs and DOCX files of patient records
2. **Embedding**: Convert text to vector embeddings for semantic search
3. **Retrieval**: Find relevant information from the knowledge base
4. **Chains**: Orchestrate LLM prompts and interactions
5. **API**: Backend services for accessing the model
6. **Frontend**: User interface for healthcare providers

## Technical Components

- **LangChain**: Framework for developing applications powered by language models
- **OpenAI**: Provides embedding and completion models
- **ChromaDB**: Vector database for storing and retrieving embeddings
- **FastAPI**: Backend API framework
- **Streamlit**: Frontend UI framework
- **Docker**: Containerization for easy deployment

## Setup

### Prerequisites
- Python 3.8 or newer
- OpenAI API key or compatible LLM API
- Docker and Docker Compose (optional, for containerized deployment)

### Installation

#### Local Setup

```bash
# Clone the repository
git clone [repository-url]
cd patientcare-assistant

# Run the setup script (creates venv and installs dependencies)
chmod +x setup_python3.sh
./setup_python3.sh

# Activate the virtual environment if not already activated
source venv_py3/bin/activate  # On Windows: venv_py3\Scripts\activate

# Configure environment variables
cp src/.env.example src/.env
# Edit src/.env to add your OpenAI API key

# Process sample documents
python src/main.py --process

# Start the application
python src/main.py --api --frontend

# Or use the control script to manage servers
./control.sh --start    # Start both servers
./control.sh --stop     # Stop both servers
./control.sh --restart  # Restart both servers
./control.sh --status   # Check server status
```

# Configure environment variables
cp src/.env.example src/.env
# Edit src/.env to add your OpenAI API key

# Process sample documents
python src/main.py --process

# Start the application
python src/main.py --api --frontend
```

#### Option 3: Docker Deployment

```bash
# Clone the repository
git clone [repository-url]
cd patientcare-assistant

# Configure environment variables
cp src/.env.example src/.env
# Edit src/.env to add your OpenAI API key

# Build and start the containers
docker-compose up -d

# Access the application
# API: http://localhost:8000
# Frontend: http://localhost:8501
```

## Usage

1. **Login**: Access the web interface at http://localhost:8501 and log in
2. **Upload Documents**: Upload patient documents in the Analysis page
3. **Search Patients**: Use the Patient Search page to find and view patient information
4. **Ask Questions**: Use the Q&A page to ask natural language questions about patients
5. **Generate Reports**: Generate summaries and health risk assessments

### Server Management

The application includes a robust server management system with a command-line interface.

#### Command Line Control

You can use the improved command-line control script to manage the API and frontend servers:

```bash
# Start both servers
./control.sh --start

# Stop both servers
./control.sh --stop

# Restart both servers
./control.sh --restart

# Check server status with detailed information
./control.sh --status --verbose

# Target specific servers
./control.sh --start --api     # Start only API server
./control.sh --restart --frontend  # Restart only Frontend server
```

For complete documentation on server management, see [Server Management Guide](docs/server-management.md).
./control.sh --status

# Control only the API server
./control.sh --start --api
./control.sh --stop --api
./control.sh --restart --api

# Control only the frontend server
./control.sh --start --frontend
./control.sh --stop --frontend
./control.sh --restart --frontend
```

## API Documentation

The API is available at http://localhost:8000 with the following endpoints:

- `GET /`: API status check
- `POST /answer`: Answer medical questions
- `POST /summary`: Generate patient summaries
- `POST /health-issues`: Identify potential health issues

## Development

### Project Structure

```
patientcare-assistant/
├─ README.md
├─ requirements.txt
├─ data/
│  ├─ raw/          # Original patient documents
│  └─ processed/    # Processed chunks and embeddings
├─ src/
│  ├─ ingestion/    # Document processing
│  ├─ embedding/    # Vector embedding generation
│  ├─ retriever/    # Information retrieval
│  ├─ chains/       # LLM prompt orchestration
│  ├─ api/          # FastAPI backend
│  └─ frontend/     # Streamlit UI
├─ tests/           # Unit tests
└─ docs/            # Documentation
```

### Running Tests

```bash
pytest tests/
```

## Security and Privacy

This application is designed to handle sensitive medical information:

- All data is processed and stored locally
- No patient data is sent to external services except for the LLM API
- Implement proper access controls in production environments
- Follow HIPAA guidelines when deploying in healthcare settings

## License

MIT License

## Acknowledgments

- LangChain for providing the frameworks for LLM application development
- OpenAI for providing the embedding and completion models
- Streamlit for the interactive frontend framework
