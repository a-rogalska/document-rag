# Document RAG
This is a simple RAG system for tax documents processing, implemented in Azure. The system includes following components:
- **Data processing pipeline**: The incoming documents are automatically processed by Azure Function to extract structured data using Document AI and classify into tax-relevant categories. Documents are then stored in a blob storage, pooled by a Azure AI Search every 5 minutes. Azure AI Search is used to store document in a Vector Database and retrieve relevant chunks for a query.
- **RAG**: A user can ask questions to previusly processed documents. A user's query is embedded with an Embedding Model and pushed to an LLM together with retrieved chunks to generate an answer.

## System architecture
![](/files/diagram.png)

## Prerequisites
Ensure you have the following installed:

- Python 3.13
- uv installed

## Installation
1. Clone this repository
```bash
git clone https://github.com/a-rogalska/document-rag.git
cd document-rag
```

2. Add necessary environment variables to .env file

LangSmith env variables for tracing are optional

3. Install packages
```bash
uv sync
```

4. Run streamlit app
```bash
#Windows
.\.venv\Scripts\activate
# execute this in root of the project
streamlit run .\src\applications\document_rag\app.py
```

#### Run tests
```bash
#Windows
.\.venv\Scripts\activate
cd .\tests\document_rag\
pytest
```

## Monitoring & Evaluation
**Data processing pipeline**:
- Azure Funtion can be monitored via logging and Application Insights.
- Even though classification works well with sample documents, it can be improved by better separating classes and adding description to a LLM call.

**RAG**:
- The RAG system can be monitored using LangSmith by adding the corresponding environment variables.
- The chatbot can accurately answer questions about documents based on retrieved chunks from Azure AI Search service.

## Improvement ideas
- Add proper tests
- Add prompt injection protection, validation and guardrails, e.g [Rebuff](https://www.rebuff.ai/)
- Incorporate Tax Law Documentation as a data source in a Vector Store
- Use combination of dense and sparse embedding
- Use hybrid search (vector + keyword) and semantic reranking
- Decouple text extraction from classification
- Store classification results in a table storage instead of document's metadata