import logging
import os

from azure.storage.blob import BlobServiceClient


class StorageClient:
    _conn_str = os.environ["AzureWebJobsStorage"]
    _container = "documents"

    def __init__(self) -> None:
        self.blob_service_client = BlobServiceClient.from_connection_string(
            self._conn_str)

    def get_filename(self, blob_name: str, container_name: str):
        logging.info(f"Geting filename for {blob_name} in container {container_name}")
        blob_client = self.blob_service_client.get_blob_client(
            container=container_name, blob=blob_name)
        metadata = blob_client.get_blob_properties().metadata
        return metadata.get("filename")

    def blob_exists(self, blob_name: str) -> bool:
        blob_client = self.blob_service_client.get_blob_client(
            container=self._container, blob=blob_name)
        return blob_client.exists()

    def upload_blob(self, data: str, blob_name: str, metadata: dict | None = None) -> None:
        blob_client = self.blob_service_client.get_blob_client(
            container=self._container, blob=blob_name)
        if blob_client.exists():
            logging.info(f"Blob '{blob_name}' already exists. Skipping upload.")
            return

        logging.info(f"Uploading Blob '{blob_name}'")
        blob_client.upload_blob(data, blob_type="BlockBlob", metadata=metadata)
