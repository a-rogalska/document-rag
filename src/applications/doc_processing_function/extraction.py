import logging
import os

from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import DocumentAnalysisFeature
from azure.core.credentials import AzureKeyCredential

DOCUMENTINTELLIGENCE_ENDPOINT = os.getenv("DOCUMENTINTELLIGENCE_ENDPOINT")
DOCUMENTINTELLIGENCE_API_KEY = os.getenv("DOCUMENTINTELLIGENCE_API_KEY")


class ExtractionClient:
    def __init__(self) -> None:
        self.extraction_client = DocumentIntelligenceClient(
            endpoint=DOCUMENTINTELLIGENCE_ENDPOINT, credential=AzureKeyCredential(DOCUMENTINTELLIGENCE_API_KEY))

    def extract(self, file_bytes: bytes) -> dict:
        logging.info(f"Extracting data from a file")
        poller = self.extraction_client.begin_analyze_document(
            "prebuilt-layout", body=file_bytes, features=[DocumentAnalysisFeature.KEY_VALUE_PAIRS])
        analyze_result = poller.result().as_dict()
        return analyze_result
