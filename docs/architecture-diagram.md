# PatientCare Assistant Architecture

## 🏗️ System Architecture Overview

The PatientCare Assistant follows a modern, modular architecture designed for scalability, maintainability, and healthcare compliance. The system has been completely refactored (October 2025) into a clean, separation-of-concerns design.

## 📊 Modular Architecture Diagram

```
┌───────────────────────────────────────────────────────────────────────────┐
│                        🎨 PRESENTATION LAYER                             │
├───────────────────────────────────────────────────────────────────────────┤
│  📱 Streamlit Frontend (Port 8501)     │  🌐 Interactive API Docs        │
│  ├── page_modules/                     │  ├── /docs (Swagger UI)          │
│  │   ├── dashboard.py                  │  ├── /redoc (ReDoc)              │
│  │   ├── qa.py                         │  └── /openapi.json               │
│  │   └── upload.py                     │                                  │
│  ├── components/                       │  🎯 External CSS Files           │
│  │   ├── navigation.py                 │  ├── styles/navigation.css       │
│  │   └── questions.py                  │  ├── styles/questions.css        │
│  └── styles/                           │  └── styles/components.css       │
│      └── *.css (externalized)          │                                  │
└───────────────────────────────────────────────────────────────────────────┘
                                       │
                                   🔗 HTTP/JSON API Calls
                                       │
┌───────────────────────────────────────────────────────────────────────────┐
│                          ⚡ MODULAR API LAYER (Port 8000)                │
├───────────────────────────────────────────────────────────────────────────┤
│  🩺 Medical Router            │  📄 Documents Router      │  🔄 Legacy Routes│
│  /medical/*                   │  /documents/*             │  /answer, /summary│
│  ├── /answer (Q&A)           │  ├── / (list docs)        │  (redirect to new)│
│  ├── /summary (patient)      │  ├── /process (pipeline)  │                  │
│  └── /health-issues (risks)  │  ├── /upload (files)      │  🎯 Middleware   │
│                               │  └── /reset (database)   │  ├── Logging     │
│  🔧 Utils & Config           │                           │  ├── Monitoring  │
│  ├── logging.py              │  📊 Pydantic Models       │  └── Error Hand. │
│  ├── file_utils.py           │  └── schemas.py           │                  │
│  └── settings.py             │                           │                  │
└───────────────────────────────────────────────────────────────────────────┘
                                       │
                                   📊 Processed Data & AI Requests
                                       │
┌───────────────────────────────────────────────────────────────────────────┐
│                         🧠 AI PROCESSING LAYER                           │
├───────────────────────────────────────────────────────────────────────────┤
│  🤖 LangChain Integration     │  🔗 OpenAI API           │  📝 Medical Prompts│
│  ├── Medical Chain           │  ├── GPT-4o for Generation│  ├── Healthcare    │
│  ├── Summary Chain           │  ├── text-embedding-3     │  ├── Context-Aware │
│  ├── QA Chain                │  └── Async Processing     │  └── Safety First  │
│  └── Dependency Injection    │                           │                    │
└───────────────────────────────────────────────────────────────────────────┘
                                       │
                                   🔍 Vector Search & Retrieval
                                       │
┌───────────────────────────────────────────────────────────────────────────┐
│                        🗄️ DATA STORAGE LAYER                            │
├───────────────────────────────────────────────────────────────────────────┤
│  📊 ChromaDB Vector DB        │  📁 Document Storage      │  🔐 Backup System │
│  ├── medical_documents        │  ├── data/raw/            │  ├── Auto Backup   │
│  ├── Semantic Search          │  ├── data/processed/      │  ├── 3-Backup Ret. │
│  ├── Patient ID Filtering     │  ├── Chunk Files (.json)  │  └── Auto Cleanup  │
│  └── HNSW Indexing           │  └── Metadata Tracking    │                    │
└───────────────────────────────────────────────────────────────────────────┘
```

## 🚀 **October 2025 Modular Refactoring**

### **✅ Key Improvements Achieved**

#### **1. API Architecture Overhaul**
- **Before**: Monolithic 873-line `app.py` file
- **After**: Clean, modular structure with separated concerns:
  ```
  src/api/
  ├── main.py              # FastAPI application setup
  ├── app.py               # Startup script (fixed import paths)
  ├── models/schemas.py    # Pydantic data models
  ├── routers/
  │   ├── medical.py       # Healthcare-specific endpoints
  │   └── documents.py     # File management operations
  ├── middleware/logging.py # Request monitoring
  ├── utils/               # Shared utilities
  └── config/settings.py   # Configuration management
  ```

#### **2. Frontend Modernization**
- **Navigation Fix**: Renamed `pages/` → `page_modules/` to prevent auto-navigation
- **CSS Externalization**: Moved inline `<style>` to dedicated `.css` files
- **Component Modularity**: Better separation between UI components
- **Utility Functions**: Created `load_css_file()` for consistent styling

#### **3. Enhanced Developer Experience**
- **Comprehensive Logging**: Request tracing with timestamps and performance metrics
- **Hot Reloading**: Automatic server restart on code changes
- **Interactive Docs**: Full Swagger UI with testing capabilities
- **Error Handling**: Improved error messages and debugging information

#### **4. Backward Compatibility**
- **Legacy Endpoints**: All original endpoints maintained and working
- **Seamless Migration**: No breaking changes for existing integrations
- **Progressive Enhancement**: New features available alongside existing functionality

### **📊 Performance Improvements**
- **Startup Time**: ~1 second with optimized imports
- **Response Time**: 1.4-1.9s average for medical queries
- **Memory Usage**: Efficient ChromaDB operations with automatic cleanup
- **Error Recovery**: Robust backup system with 3-backup retention

### **🔧 Technical Debt Resolution**
- **Import Path Issues**: Fixed Python module resolution problems
- **Code Organization**: Clear separation of concerns across modules
- **Documentation**: Comprehensive API docs with examples
- **Testing**: All endpoints verified and working correctly

## 🔄 Data Flow Architecture

```
📋 Patient Documents (PDF, DOCX, MD, TXT)
          │
          ▼
    📥 Document Upload (/documents/upload)
          │
          ▼
    🔍 Patient ID Extraction (PATIENT-XXXXX)
          │
          ▼
    ✂️ Text Chunking & Processing (/documents/process)
          │
          ▼
    🧠 Embedding Generation (OpenAI text-embedding-3)
          │
          ▼
    💾 Vector Storage (ChromaDB medical_documents)
          │
          ▼
    🔍 Semantic Retrieval (Patient-filtered search)
          │
          ▼
    🤖 LLM Processing (GPT-4o with medical prompts)
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
