from decimal import Decimal
from unittest import TestCase

from pydantic import ValidationError

from models import CSVTransactionRecord, TransactionCollection, Mutation


class MutationTest(TestCase):
    def test_assign_int(self):
        m = Mutation.validate("+1")

    def test_assign_number_with_period(self):
        m = Mutation.validate("-1.0")

    def test_assign_number_with_comma(self):
        with self.assertRaises(TypeError):
            m = Mutation.validate("-1,0")

    def test_not_a_number(self):
        with self.assertRaises(TypeError):
            m = Mutation.validate("+een")

    def test_negative_sign(self):
        m = Mutation("-1.0")

        m.validate_transaction(Decimal(1.0), Decimal(0.0), 1)

    def test_positive_sign(self):
        m = Mutation("+1.0")
        m.validate_transaction(Decimal(1.0), Decimal(2.0), 1)

    def test_unknown_sign_raises_valuerror(self):
        with self.assertRaises(ValueError):
            m = Mutation("*1.0")

            m.validate_transaction(Decimal(1.0), Decimal(2.0), 1)


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
        self.assertEqual(len(collection.valid_transactions), 1)
        self.assertEqual(len(collection.invalid_transactions), 99)
