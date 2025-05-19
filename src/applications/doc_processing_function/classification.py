import logging
import os

import numpy as np
from langchain_openai import AzureChatOpenAI
from models import Classification
from prompts import cls_prompt

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ENDPOINT = os.getenv("OPENAI_ENDPOINT")
OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION", "2024-12-01-preview")
OPENAI_DEPLOYMENT = os.getenv("OPENAI_DEPLOYMENT", "gpt-4o-mini")


class ClassificationClient:
    def __init__(self) -> None:
        llm = AzureChatOpenAI(
            azure_endpoint=OPENAI_ENDPOINT,
            api_key=OPENAI_API_KEY,
            azure_deployment=OPENAI_DEPLOYMENT,
            api_version=OPENAI_API_VERSION,
            logprobs=True,
            temperature=0
        )
        self.structured_llm = llm.with_structured_output(Classification, include_raw=True)
        self.prompt = cls_prompt

    def classify(self, raw_text: str) -> tuple[str, float]:
        logging.info(f"Classifying document")

        prompt = self.prompt.invoke({"input": raw_text})
        response = self.structured_llm.invoke(prompt)
        cls = response['parsed'].tax_category

        try:
            logprob = response["raw"].response_metadata['logprobs']['content'][4]['logprob']
            confidence = np.round(np.exp(logprob)*100, 2).item()
        except Exception as e:
            logging.info(f"Couldn't extract confidence")
            confidence = 0.

        logging.info(f"Classification result: class {cls}, confidence: {confidence}")
        return cls, confidence
