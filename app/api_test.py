from unittest import TestCase

from pydantic import ValidationError

from models import TransactionRecord, TransactionCollection


class TransactionRecordTest(TestCase):
    def test_assign_valid_iban(self):
        r = TransactionRecord.parse_obj({
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
            r = TransactionRecord.parse_obj({
                "Reference": 123465,
                "Account Number": "NL90ABNA0585647887",
                "Description": "test",
                "Start Balance": 1.0,
                "Mutation": "-1.0",
                "End Balance": 0
            })


class TransactionCollectionTest(TestCase):
    def test_unique_references(self):
        transactions = []

        for i in range(0, 100):
            transactions.append({
                "Reference": i,
                "Account Number": "NL90ABNA0585647886",
                "Description": "test",
                "Start Balance": 1.0,
                "Mutation": "-1.0",
                "End Balance": 0
            })

        collection = TransactionCollection(
            transactions=transactions
        )

        self.assertEqual(len(collection.transactions), 100)
        self.assertEqual(len(collection.failed_transactions), 0)

    def test_failures_on_reused_references(self):
        transactions = []

        for i in range(0, 100):
            transactions.append({
                "Reference": 1,
                "Account Number": "NL90ABNA0585647886",
                "Description": "test",
                "Start Balance": 1.0,
                "Mutation": "-1.0",
                "End Balance": 0
            })

        collection = TransactionCollection(
            transactions=transactions
        )

        self.assertEqual(len(collection.transactions), 100)
        self.assertEqual(len(collection.failed_transactions), 99)
