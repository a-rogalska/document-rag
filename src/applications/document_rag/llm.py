from config import settings
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureChatOpenAI
from langchain_openai import AzureOpenAIEmbeddings

llm: AzureChatOpenAI = AzureChatOpenAI(
    **settings.llm.model_dump(),
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    logprobs=True
)

embeddings: AzureOpenAIEmbeddings = AzureOpenAIEmbeddings(**settings.embedding.model_dump())

vector_store: AzureSearch = AzureSearch(
    index_name=settings.vectorstore.index_name,
    azure_search_endpoint=settings.vectorstore.azure_search_endpoint,
    azure_search_key=settings.vectorstore.azure_search_key.get_secret_value(),
    embedding_function=embeddings.embed_query,
    additional_search_client_options={"retry_total": 2},
    vector_search_dimensions=1536
)
