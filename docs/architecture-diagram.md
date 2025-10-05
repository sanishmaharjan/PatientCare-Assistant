# PatientCare Assistant Architecture

[This is a placeholder for an architecture diagram. In a real implementation, you would create a PNG file using a diagramming tool.]

## Architecture Components

```
+-------------------+
|                   |
|  Patient Records  |
|  (PDFs, DOCx)     |
|                   |
+--------+----------+
         |
         | Document Ingestion
         v
+--------+----------+     +-------------------+
|                   |     |                   |
|  Document Chunks  +---->+  Vector Database  |
|                   |     |                   |
+--------+----------+     +--------+----------+
         |                         |
         | Embedding               | Semantic Search
         v                         |
+--------+----------+              |
|                   |              |
|  Vector Embeddings+<-------------+
|                   |
+--------+----------+
         |
         | Retrieval
         v
+--------+----------+
|                   |
|  LLM Chain        |
|                   |
+--------+----------+
         |
         | Processing
         v
+--------+----------+     +-------------------+
|                   |     |                   |
|  API Server       +---->+  Web Frontend     |
|                   |     |                   |
+-------------------+     +-------------------+
```

## Data Flow

1. **Document Ingestion**: Patient records are processed and chunked
2. **Embedding Generation**: Text chunks are converted to vector embeddings
3. **Vector Database**: Embeddings are stored with metadata
4. **Retrieval**: Relevant information is fetched based on queries
5. **LLM Processing**: Language models generate answers and insights
6. **API & Frontend**: Results are delivered through API and web interface
