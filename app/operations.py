from typing import Dict, Iterable, List

import xmltodict
import csv
from fastapi import UploadFile
from models import TransactionCollection


def load_file(file: UploadFile) -> Iterable:
    """
    Loads a file into a regular dict
    """
    if file.content_type == "text/csv":
        return load_csv(file.file)
    elif file.content_type == "text/xml":
        return load_xml(file.file)


def load_csv(csv_content) -> Iterable:
    """
    Loads CSV into a generic dict
    """
    csv_fo = map(lambda x: x.decode(), csv_content.readlines())
    df = csv.DictReader(csv_fo)

    return list(df)


def load_xml(xml_file) -> Iterable:
    """
    Loads XML into a generic dict
    """
    parsed_data = xmltodict.parse(xml_file)
    rows = parsed_data['records']['record']

    for item in rows:
        item['reference'] = item.pop('@reference')

    return rows


def parse_to_models(raw_items: Iterable[Dict], type: str) -> TransactionCollection:
    """
    Takes a list of raw transactions and parses them to a TransactionCollection
    """
    collection = TransactionCollection(
        content_type=type,
        raw_transactions=raw_items
    )

    collection.process()

    return collection
