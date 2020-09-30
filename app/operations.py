from typing import Dict, Iterable, TextIO

import pandas as pd
from fastapi import UploadFile

from models import TransactionCollection


def load_file(file: UploadFile) -> Iterable:
    """
    Loads a file into a regular dict
    """
    if file.content_type == "text/csv":
        return load_csv(file.file)


def load_csv(csv_content) -> Iterable:
    """
    Loads CSV into a generic dict
    """
    df = pd.read_csv(csv_content)

    return df.to_dict(orient="records")


def load_xml(xml_file) -> Iterable:
    """
    Loads XML into a generic dict
    """
    pass


def parse_to_models(raw_items: Iterable[Dict]) -> TransactionCollection:
    """
    Takes a list of raw transactions and parses them to a TransactionCollection
    """
    collection = TransactionCollection(
        raw_transactions=raw_items
    )

    collection.process()

    return collection
