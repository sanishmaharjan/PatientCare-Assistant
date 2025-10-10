# PatientCare Assistant

A production-ready, generative AI-powered assistant for healthcare providers to quickly retrieve and analyze patient information from medical documents.

## 🎯 Overview

PatientCare Assistant is a comprehensive healthcare AI solution that helps healthcare providers:
- **Extract and organize** information from patient documents automatically
- **Answer questions** about patient medical history using natural language
- **Generate comprehensive summaries** of patient data with source citations
- **Identify potential health issues** and risks based on patient records
- **Provide evidence-based insights** with full traceability to source documents

## ✨ Key Features

### 🔄 **Advanced Document Processing**
- **Multi-format support**: PDF, DOCX, Markdown, and text documents
- **Intelligent chunking**: Optimized text segmentation for better retrieval
- **Automatic backup system**: 3-backup retention with automatic cleanup
- **ChromaDB integration**: High-performance vector database with conflict resolution

### 🔍 **Intelligent Search & Retrieval**
- **Semantic search**: Natural language queries with context awareness
- **Patient-specific filtering**: Automatically extract and filter by patient IDs
- **Source attribution**: Full traceability to original documents
- **Multi-document synthesis**: Combine information from multiple sources

### 🩺 **Healthcare-Focused AI**
- **Medical Q&A**: Specialized prompts for medical contexts
- **Patient summaries**: Comprehensive health status overviews
- **Risk assessment**: Identify potential health concerns
- **Treatment insights**: Medication and care plan analysis

### 🖥️ **Professional Interface**
- **Healthcare provider dashboard**: Patient-centric view with metrics
- **Interactive Q&A**: Chat interface with suggested medical questions
- **Document management**: Upload, process, and organize medical records
- **Real-time processing**: Live status updates and progress tracking

### 🛡️ **Enterprise-Ready**
- **Robust error handling**: Comprehensive backup and recovery systems
- **Performance monitoring**: Detailed logging and telemetry
- **Scalable architecture**: Docker containerization support
- **Clean codebase**: Thoroughly tested and documented

## 🏗️ Architecture

The application follows a robust, modular architecture designed for healthcare environments:

### **Core Components**

1. **📄 Data Ingestion Layer**
   - **Document Processor**: Intelligent parsing of PDF, DOCX, MD, and TXT files
   - **Patient ID Extraction**: Automatic identification of patient identifiers
   - **Text Chunking**: Optimized segmentation for semantic search
   - **Metadata Enrichment**: Source tracking and document attribution

2. **🧠 AI & Embedding Layer**
   - **OpenAI Embeddings**: High-quality vector representations
   - **ChromaDB Vector Store**: Persistent, high-performance vector database
   - **Conflict Resolution**: Robust handling of database locks and process conflicts
   - **Backup System**: Automatic backup creation and restoration

3. **🔍 Retrieval & Chain Layer**
   - **Semantic Retrieval**: Context-aware document search
   - **Medical Chains**: Specialized prompts for healthcare queries
   - **Source Attribution**: Full traceability to original documents
   - **Context Synthesis**: Multi-document information combination

4. **🌐 API Layer**
   - **FastAPI Backend**: Modern, async API with automatic documentation
   - **Enhanced Error Handling**: Comprehensive error recovery and logging
   - **Telemetry Filtering**: Clean log output with performance monitoring
   - **RESTful Endpoints**: Standard HTTP interface for all operations

5. **🖥️ Frontend Layer**
   - **Streamlit Interface**: Professional healthcare provider dashboard
   - **Real-time Updates**: Live processing status and progress tracking
   - **Interactive Components**: Chat interface, file management, patient cards
   - **Responsive Design**: Optimized for various screen sizes

### **Technology Stack**

- **🔗 LangChain**: Advanced framework for LLM application development
- **🤖 OpenAI**: GPT models for text generation and embeddings
- **🗄️ ChromaDB**: Vector database with persistence and backup capabilities
- **⚡ FastAPI**: High-performance async API framework with auto-documentation
- **🎨 Streamlit**: Modern web interface framework for data applications
- **🐳 Docker**: Containerization for consistent deployments
- **🧪 Pytest**: Comprehensive testing framework with healthcare-specific tests

## Setup

### Prerequisites
- Python 3.8 or newer (currently optimized for Python 3.13+)
- OpenAI API key or compatible LLM API
- Docker and Docker Compose (optional, for containerized deployment)

### Installation

#### Local Setup

```bash
# Clone the repository
git clone git@github.com:sanishmaharjan/PatientCare-Assistant.git
cd patientcare-assistant

# Run the setup script (creates venv and installs dependencies)
chmod +x scripts/setup_python3.sh
./scripts/setup_python3.sh

# Activate the virtual environment if not already activated
source venv_py3/bin/activate  # On Windows: venv_py3\Scripts\activate

# Configure environment variables
cp src/.env.example src/.env
# Edit src/.env to add your OpenAI API key

# Run the application (all-in-one launcher)
chmod +x scripts/run_all.sh
./scripts/run_all.sh

# Or use individual scripts for more control:
# Process documents only
./scripts/run_processing.sh

# Start API and frontend servers
./scripts/run_servers.sh

# Or use the control script for server management
./scripts/control.sh --start    # Start both servers
./scripts/control.sh --stop     # Stop both servers
./scripts/control.sh --status   # Check server status

# See docs/launcher-scripts.md for more options
```

#### Option 2: Manual Setup

```bash
# Clone the repository
git clone [repository-url]
cd patientcare-assistant

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

## 🚀 Usage

1. **🏠 Access Dashboard**: Open the web interface at http://localhost:8501 to view the dashboard
2. **📁 Upload Documents**: Upload patient documents in the Upload Data page
3. **👥 Patient Information**: View and analyze patient information directly from the Dashboard
4. **❓ Ask Questions**: Use the Q&A page to ask natural language questions about patients
5. **📊 Generate Reports**: Generate summaries and health risk assessments

### 🎛️ Server Management

The application includes a robust server management system with a comprehensive command-line interface.

#### Command Line Control

Use the improved control script to manage API and frontend servers:

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
./control.sh --start --api          # Start only API server
./control.sh --restart --frontend   # Restart only Frontend server
./control.sh --stop --api           # Stop only API server
```

For complete server management documentation, see [Server Management Guide](docs/server-management.md).

## 📁 Scripts Directory

All shell scripts are organized in the `scripts/` directory. For a complete overview of available scripts and their usage, see [Scripts README](scripts/README.md).

**Quick Reference:**
- `./scripts/run_all.sh` - Complete system setup and launch
- `./scripts/control.sh --status` - Check server status  
- `./scripts/run_processing.sh` - Process documents only
- `./scripts/setup_python3.sh` - Initial environment setup
./control.sh --stop --frontend
./control.sh --restart --frontend

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
├─ scripts/         # Shell scripts for setup and management
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
# Use the test script
./scripts/run_tests.sh

# Or run directly with pytest
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
