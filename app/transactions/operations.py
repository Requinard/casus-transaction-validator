import csv
from typing import Dict, Iterable, IO

import xmltodict
from fastapi import UploadFile

from .models import TransactionCollection, AcceptedContentTypes


def load_file(file: UploadFile) -> Iterable:
    """
    Loads a file into a regular dict
    """
    content_type = AcceptedContentTypes(file.content_type)

    if content_type == AcceptedContentTypes.CSV:
        return load_csv(file.file)
    elif content_type == AcceptedContentTypes.XML:
        return load_xml(file.file)

    raise ValueError(f"Cannot parse {content_type} as a file!")


def load_csv(csv_file: IO) -> Iterable:
    """
    Loads CSV into a generic dict
    """
    csv_fo = map(lambda x: x.decode(), csv_file.readlines())
    dict_reader = csv.DictReader(csv_fo)

    # Manually turn this into a list of dicts
    return list(dict_reader)


def load_xml(xml_file: IO) -> Iterable:
    """
    Loads XML into a generic dict
    """
    parsed_data = xmltodict.parse(xml_file)
    rows = parsed_data['records']['record']

    for item in rows:
        # remove @-style reference as this does not work nicely with python dicts
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

    # If we need to store the results of this transaction in a DB we would do this here, before returning

    return collection
