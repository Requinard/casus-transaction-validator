from unittest import TestCase

from pydantic import ValidationError

from transactions.models import CSVTransactionRecord


class CSVTransactionRecordTest(TestCase):
    def test_assign_valid_iban(self):
        r = CSVTransactionRecord.parse_obj({
            "Reference": 123465,
            "Account Number": "NL90ABNA0585647886",
            "Description": "test",
            "Start Balance": 1.0,
            "Mutation": "-1.0",
            "End Balance": 0
        })

        self.assertIsNotNone(r)

    def test_throws_on_invalid_iban(self):
        with self.assertRaises(ValidationError):
            r = CSVTransactionRecord.parse_obj({
                "Reference": 123465,
                "Account Number": "NL90ABNA0585647887",
                "Description": "test",
                "Start Balance": 1.0,
                "Mutation": "-1.0",
                "End Balance": 0
            })

    def test_valid_mutation_works(self):
        r = CSVTransactionRecord.parse_obj({
            "Reference": 123465,
            "Account Number": "NL90ABNA0585647886",
            "Description": "test",
            "Start Balance": 1.0,
            "Mutation": "-1.0",
            "End Balance": 0
        })

        self.assertIsNotNone(r)

    def test_invalid_mutation_throws(self):
        with self.assertRaises(ValidationError):
            r = CSVTransactionRecord.parse_obj({
                "Reference": 123465,
                "Account Number": "NL90ABNA0585647887",
                "Description": "test",
                "Start Balance": 1.0,
                "Mutation": "-1.0",
                "End Balance": -1.0
            })
