# PatientCare Assistant Architecture

## 🏗️ System Architecture Overview

The PatientCare Assistant follows a modern, layered architecture designed for scalability, reliability, and healthcare compliance.

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        🎨 PRESENTATION LAYER                            │
├─────────────────────────────────────────────────────────────────────────┤
│  📱 Streamlit Frontend     │  🌐 FastAPI Web Interface  │  📋 REST API   │
│  - Interactive Dashboard  │  - Flask Compatibility     │  - JSON/HTTP   │
│  - Real-time Updates      │  - Session Management      │  - Auto-docs   │
└─────────────────────────────────────────────────────────────────────────┘
                                       │
                                   🔗 HTTP/JSON
                                       │
┌─────────────────────────────────────────────────────────────────────────┐
│                          ⚡ API LAYER                                   │
├─────────────────────────────────────────────────────────────────────────┤
│  🔍 Query Endpoint        │  📄 Summary Endpoint      │  🏥 Health Issues│
│  /answer                  │  /summary                 │  /health-issues  │
│  - Natural Language Q&A   │  - Patient Summaries      │  - Risk Analysis │
│  - Context Retrieval      │  - Medical History        │  - Alerts        │
└─────────────────────────────────────────────────────────────────────────┘
                                       │
                                   📊 Processed Data
                                       │
┌─────────────────────────────────────────────────────────────────────────┐
│                         🧠 AI PROCESSING LAYER                          │
├─────────────────────────────────────────────────────────────────────────┤
│  🤖 LangChain Chains      │  🔗 OpenAI Integration    │  📝 Prompt Eng. │
│  - Medical Q&A Chain      │  - GPT-4 for Generation   │  - Healthcare    │
│  - Summary Chain          │  - Text-embedding-3       │  - Context-Aware │
│  - Health Issues Chain    │  - Async Processing       │  - Safety First  │
└─────────────────────────────────────────────────────────────────────────┘
                                       │
                                   🔍 Vector Search
                                       │
┌─────────────────────────────────────────────────────────────────────────┐
│                        🗄️ DATA STORAGE LAYER                           │
├─────────────────────────────────────────────────────────────────────────┤
│  📊 ChromaDB Vector DB    │  📁 Document Storage      │  🔐 Backup System│
│  - Semantic Search        │  - Raw Documents          │  - Auto Backup   │
│  - Persistent Storage     │  - Processed Chunks       │  - Recovery      │
│  - HNSW Indexing         │  - Metadata Tracking      │  - Versioning    │
└─────────────────────────────────────────────────────────────────────────┘
                                       │
                                   📥 Document Input
                                       │
┌─────────────────────────────────────────────────────────────────────────┐
│                       📥 DATA INGESTION LAYER                           │
├─────────────────────────────────────────────────────────────────────────┤
│  📄 Document Loaders      │  ✂️ Text Splitters        │  🔍 ID Extraction│
│  - PDF (PyPDF)           │  - Recursive Chunking     │  - Patient IDs    │
│  - DOCX (docx2txt)       │  - Overlap Strategy       │  - Regex Patterns │
│  - TXT/MD (TextLoader)   │  - Semantic Boundaries    │  - Validation     │
└─────────────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow Architecture

```
📋 Patient Documents
          │
          ▼
    📥 Document Upload
          │
          ▼
    🔍 Patient ID Extraction
          │
          ▼
    ✂️ Text Chunking & Processing
          │
          ▼
    🧠 Embedding Generation (OpenAI)
          │
          ▼
    💾 Vector Storage (ChromaDB)
          │
          ▼
    🔍 Semantic Retrieval
          │
          ▼
    🤖 LLM Processing (GPT-4)
          │
          ▼
    📊 Structured Response
          │
          ▼
    🎨 Frontend Display
```
## 🏛️ Detailed Component Breakdown

### 1. **📥 Data Ingestion Layer**
- **Document Processors**: Intelligent parsing for multiple formats
- **Patient ID Extraction**: Automated identification with validation
- **Text Chunking**: Optimized segmentation for semantic coherence
- **Metadata Enrichment**: Source tracking and document attribution

### 2. **🗄️ Data Storage Layer**
- **ChromaDB Vector Database**: High-performance semantic search
- **Document Storage**: Raw and processed document management
- **Backup System**: Automated backup creation and restoration
- **Conflict Resolution**: Robust handling of database locks

### 3. **🧠 AI Processing Layer**
- **LangChain Framework**: Advanced prompt engineering and chain orchestration
- **OpenAI Integration**: GPT-4 for generation, text-embedding-3 for vectors
- **Medical Chains**: Specialized prompts for healthcare scenarios
- **Context Synthesis**: Multi-document information combination

### 4. **⚡ API Layer**
- **FastAPI Framework**: High-performance async API with auto-documentation
- **RESTful Endpoints**: Standardized interfaces for all operations
- **Error Handling**: Comprehensive error management and logging
- **Rate Limiting**: API protection and usage monitoring

### 5. **🎨 Presentation Layer**
- **Streamlit Frontend**: Modern, interactive web interface
- **Flask Compatibility**: Legacy support for existing integrations
- **Real-time Updates**: Live data refresh and status monitoring
- **Responsive Design**: Mobile-friendly interface design

## 🔐 Security & Compliance

- **Local Processing**: All sensitive data processed locally
- **HIPAA Considerations**: Designed with healthcare privacy in mind
- **Access Controls**: Role-based permissions and authentication
- **Audit Logging**: Comprehensive activity tracking
- **Data Encryption**: Secure storage and transmission protocols

## 🚀 Performance & Scalability

- **Async Processing**: Non-blocking operations for better performance
- **Vector Indexing**: HNSW algorithm for fast similarity search
- **Caching Strategy**: Intelligent caching of embeddings and results
- **Resource Management**: Efficient memory and CPU utilization
- **Horizontal Scaling**: Docker-ready for container orchestration

## 🔧 Technology Stack

| Layer | Technologies |
|-------|-------------|
| **Frontend** | Streamlit, Flask, HTML/CSS/JavaScript |
| **API** | FastAPI, Uvicorn, Pydantic |
| **AI/ML** | LangChain, OpenAI GPT-4, OpenAI Embeddings |
| **Database** | ChromaDB, Vector Storage, JSON |
| **Processing** | Python 3.8+, Async/Await, Pandas |
| **DevOps** | Docker, Docker Compose, Shell Scripts |
| **Testing** | Pytest, Unit Tests, Integration Tests |

## 📊 Data Flow Phases

1. **📄 Document Ingestion**: Patient records uploaded and validated
2. **🔍 ID Extraction**: Patient identifiers automatically detected
3. **✂️ Text Processing**: Documents chunked with semantic awareness
4. **🧠 Embedding Generation**: Text converted to high-dimensional vectors
5. **💾 Vector Storage**: Embeddings stored with metadata in ChromaDB
6. **🔍 Semantic Retrieval**: Relevant information retrieved based on queries
7. **🤖 LLM Processing**: Context-aware responses generated using GPT-4
8. **📊 Response Formatting**: Structured output with source attribution
9. **🎨 UI Presentation**: Results displayed in user-friendly interface
