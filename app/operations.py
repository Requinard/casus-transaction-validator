import csv
from typing import Dict, Iterable

from fastapi import UploadFile

from models import TransactionCollection


def load_file(file: UploadFile) -> Dict:
    """
    Loads a file into a regular dict
    """
    if file.content_type == "text/csv":
        return load_csv(file.file)


def load_csv(csv_file) -> Iterable:
    """
    Loads CSV into a generic dict
    """
    with open(csv_file, 'r') as f:
        return csv.DictReader(f)


def load_xml(xml_file) -> Iterable:
    """
    Loads XML into a generic dict
    """
    pass


def parse_to_models(raw_items: Iterable[Dict]) -> TransactionCollection:
    """
    Takes a list of raw transactions and parses them to a TransactionCollection
    """
    return TransactionCollection.construct(
        transactions=raw_items
    )
