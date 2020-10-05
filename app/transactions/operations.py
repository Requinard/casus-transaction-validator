import csv
import json
from typing import Dict, Iterable, IO

import xmltodict

from .models import TransactionCollection, AcceptedContentTypes


def load_file(content_type: AcceptedContentTypes, file: IO) -> Iterable:
    """
    Loads a file into a regular dict
    """
    if content_type == AcceptedContentTypes.CSV:
        return load_csv(file)
    elif content_type == AcceptedContentTypes.XML:
        return load_xml(file)
    elif content_type == AcceptedContentTypes.JSON:
        return json.load(file)

    raise ValueError(f"Cannot parse {content_type} as a file!")


def load_csv(csv_file: IO, encoding: str = 'ISO-8859-1') -> Iterable:
    """
    Loads CSV into a generic dict
    """
    csv_fo = map(lambda x: x.decode(encoding), csv_file.readlines())
    dict_reader = csv.DictReader(csv_fo)

    result = list(dict_reader)

    if len(result) == 0:
        raise ValueError(f"The decoded CSV file has no rows. Is the file encoded properly? It should be {encoding}")

    # Manually turn this into a list of dicts
    return result


def load_xml(xml_file: IO, encoding: str = 'UTF-8') -> Iterable:
    """
    Loads XML into a generic dict
    """
    parsed_data = xmltodict.parse(xml_file, encoding=encoding)
    data_rows = parsed_data['records']['record']
    finished_rows = []

    for item in data_rows:
        # remove @-style reference as this does not work nicely with python dicts
        item['reference'] = item.pop('@reference')

        finished_rows.append(dict(item))

    return finished_rows


def parse_and_process(raw_items: Iterable[Dict], type: AcceptedContentTypes) -> TransactionCollection:
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
