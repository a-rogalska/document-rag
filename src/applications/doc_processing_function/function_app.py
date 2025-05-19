import json
import logging
import os

import azure.functions as func

from classification import ClassificationClient
from extraction import ExtractionClient
from storage import StorageClient

app = func.FunctionApp()
storage_client = StorageClient()
extraction_client = ExtractionClient()
classification_client = ClassificationClient()


@app.blob_trigger(arg_name="blob", path="files/{name}",
                  connection="AzureWebJobsStorage")
def doc_processing(blob: func.InputStream):
    logging.info(f"Starting processing blob: {blob.name}, size: {blob.length} bytes")

    filename = os.path.basename(blob.name)
    new_filename = filename + ".json"
    if storage_client.blob_exists(blob_name=new_filename):
        logging.info(f"Blob '{blob.name}' already processed. Skipping processing.")
        return

    orig_filename = storage_client.get_filename(blob_name=filename, container_name="files")

    file_bytes = blob.read()
    extracted_doc = extraction_client.extract(file_bytes=file_bytes)
    doc_text = extracted_doc["content"]

    cls, prob = classification_client.classify(doc_text)
    review_flag = prob < 70.
    metadata_text = f"\n-----\nMetadata:\nClass: {cls}, Confidence: {prob}%, Flagged for manual review: {review_flag}"

    metadata = {
        "filename": orig_filename,
        "cls": cls,
        "confidence": str(prob),
        "review": str(review_flag),
    }
    document = {
        **metadata,
        "content": doc_text + metadata_text,
        "text": doc_text,
        "kv_pairs": extracted_doc["keyValuePairs"],
        "doc_pages": extracted_doc["pages"],
        "doc_tables": extracted_doc["tables"],
        "doc_paragraphs": extracted_doc["paragraphs"]
    }
    json_doc = json.dumps(document)
    storage_client.upload_blob(data=json_doc, blob_name=new_filename, metadata=metadata)
