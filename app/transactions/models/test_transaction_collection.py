from unittest import TestCase

from .transaction_collection import TransactionCollection


class TransactionCollectionTest(TestCase):
    def test_unique_references(self):
        transactions = []

        for i in range(1, 101):
            transactions.append({
                "Reference": i,
                "Account Number": "NL90ABNA0585647886",
                "Description": "test",
                "Start Balance": 1.0,
                "Mutation": "-1.0",
                "End Balance": 0
            })

        collection = TransactionCollection(
            raw_transactions=transactions,
            content_type="text/csv"
        )

        collection.process()

        self.assertEqual(len(collection.raw_transactions), 100)
        self.assertEqual(len(collection.valid_transactions), 100)
        self.assertEqual(len(collection.invalid_transactions), 0)

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
            raw_transactions=transactions,
            content_type="text/csv"
        )

        collection.process()

        self.assertEqual(len(collection.raw_transactions), 100)
        self.assertEqual(len(collection.valid_transactions), 0)
        self.assertEqual(len(collection.invalid_transactions), 100)
