# Document RAG
This is a RAG system for tax documents processing, hosted in Azure. The cloud-native implementation was prioritized while using free options for most services. The system includes the following components:
- **Data processing pipeline**: The incoming documents are uploaded to a Blob Storage and automatically processed by an Azure Function to extract structured data using Azure Document AI and classify them into tax-relevant categories. Documents are then stored in a Blob Storage, polled by an Azure AI Search every 5 minutes. Azure AI Search is used to store documents in a Vector Database and retrieve relevant chunks for a query.
- **RAG**: A user can ask questions about previously processed documents. A user's query is embedded with an Embedding Model and pushed to an LLM together with retrieved chunks to generate an answer. The web app is hosted as an Azure Web App, using a container image uploaded to the Docker Hub.

## System architecture
![](/files/diagram.png)

## Prerequisites
Ensure you have installed:

- Python 3.13
- uv installed

## Installation
1. Clone this repository
```bash
git clone https://github.com/a-rogalska/document-rag.git
cd document-rag
```

2. Add necessary environment variables to the .env file

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

## Design decisions
- Blob storage is the best way to store both structured and unstructured data in scenarios that don't require complex read-write patterns where most operations read the entire document. It provides high-availability and scalability.
- Azure function is a good serverless option to run short workflows that can be triggered directly when a new blob is uploaded.
- AI Search is well integrated with the Azure ecosystem and allows for automatic polling, chunking, and embedding of the data. It is scalable and secure and can be used in a production environment. Also, one free tier service is allowed per subscription.
- GPT-4o-mini was used as an LLM, as it is the most cost-efficient consumption-based small model provided by Azure.
- Similarly, text-embedding-3-small is the most cost-efficient consumption-based option for an embedding model.

## Monitoring
- Azure Funtion is monitored via logging and Application Insights.
- The RAG system is monitored using LangSmith (the corresponding environment variables need to be present).

## Evaluation
- The system was evaluated manually based on the presented set of test documents and questions. 
- The system consistently extracted relevant fields with high accuracy and classified them into a correct category.
- The chatbot can accurately answer questions about documents based on retrieved chunks from the Azure AI Search service.
- As the next step, it would be beneficial to add automatic evaluation pipelines for classification, extraction, and RAG systems with labeled test data.

## Improvement ideas
- Improve test coverage and error handling.
- Add prompt injection protection, validation and guardrails, e.g [Rebuff](https://www.rebuff.ai/).
- Incorporate Tax Law Documentation as a data source in a Vector Store.
- Use combination of dense and sparse embeddings.
- Use hybrid search (vector + keyword) and semantic reranking.
- Decouple text extraction from classification.
- Store metadata of documents in a separate NoSQL storage (e.g. Azure Table Storage, Azure CosmosDB).
- Add automatic evaluation.
- Although classification performs well on sample documents, it can be further improved by enhancing class separation and including more descriptive context in the LLM call.