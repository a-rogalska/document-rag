import logging
import uuid

from azure.storage.blob import BlobServiceClient
from config import settings


class StorageClient:
    _conn_str = settings.storage.conn_str.get_secret_value()

    def __init__(self) -> None:
        self._blob_service_client = BlobServiceClient.from_connection_string(self._conn_str)

    def _generate_blob_filename(self, orig_filename: str) -> str:
        file_ext = orig_filename.split(".")[-1]
        return f"{uuid.uuid4()}.{file_ext}"

    def upload_blob(self, data: bytes, container_name: str, filename: str) -> None:
        blob_name = self._generate_blob_filename(filename)

        blob_client = self._blob_service_client.get_blob_client(container=container_name, blob=blob_name)
        if blob_client.exists():
            logging.info(f"Blob '{blob_name}' already exists. Skipping upload.")
        else:
            logging.info(f"Blob '{blob_name}' does not exist. Uploading...")
            blob_client.upload_blob(data, blob_type="BlockBlob", metadata={"filename": filename})

    def get_blobs_with_metadata(self, container_name: str) -> list:
        blob_list = self._blob_service_client.get_container_client(container_name).list_blobs(include='metadata')
        result = []
        for doc in blob_list:
            metadata = doc['metadata']
            result.append({
                "Filename": metadata.get('filename'),
                "Category": metadata.get('cls'),
                "Confidence": metadata.get('confidence'),
                "Review needed": metadata.get('review')
            })

        return result
