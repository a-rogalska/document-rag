from dotenv import load_dotenv
from pydantic import Field
from pydantic import SecretStr
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

load_dotenv()


class OpenAILLMSettings(BaseSettings):
    model: str = Field(default="gpt-4o-mini")
    api_version: str = Field(default="2024-12-01-preview")
    api_key: SecretStr
    azure_endpoint: str


class OpenAIEmbeddingSettings(BaseSettings):
    model: str = Field(default="text-embedding-3-small")
    api_version: str = Field(default="2024-12-01-preview")
    api_key: SecretStr
    azure_endpoint: str


class VectorStoreSettings(BaseSettings):
    index_name: str
    azure_search_endpoint: str
    azure_search_key: SecretStr


class StorageSettings(BaseSettings):
    conn_str: SecretStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8',
                                      env_nested_delimiter="__")
    llm: OpenAILLMSettings
    embedding: OpenAIEmbeddingSettings
    vectorstore: VectorStoreSettings
    storage: StorageSettings
    azuresearch_fields_content_vector: str
    azuresearch_fields_content: str
    azuresearch_fields_id: str
    langsmith_tracing: str | None = None
    langsmith_api_key: str | None = None
    langsmith_endpoint: str | None = None


settings = Settings()
