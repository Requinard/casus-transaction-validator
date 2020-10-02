from unittest import TestCase

from fastapi.testclient import TestClient

from api import app

client = TestClient(app)


class ValidateSingleTest(TestCase):
    url = "/transactions/validate/single"

    def test_validate_single(self):
        t = {
            "reference": 1,
            "account_number": "NL90ABNA0585647886",
            "description": "string",
            "start_balance": 1,
            "mutation": "+1.0",
            "end_balance": 2
        }

        response = client.post(self.url, json=t)
        body = response.json()

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(body['valid_transactions']), 1)
        self.assertEqual(len(body['invalid_transactions']), 0)
        self.assertEqual(len(body['raw_transactions']), 1)

    def test_validate_single_fails(self):
        t = {
            "reference": 1,
            "account_number": "NL90ABNA0585647886",
            "description": "string",
            "start_balance": 1,
            "mutation": "+1.0",
            "end_balance": 3
        }

        response = client.post(self.url, json=t)
        body = response.json()

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(body['valid_transactions']), 0)
        self.assertEqual(len(body['invalid_transactions']), 1)
        self.assertEqual(len(body['raw_transactions']), 1)


class ValidateCollectionTest(TestCase):
    url = "/transactions/validate"

    def test_validate_transactions(self):
        data = [
            {
                "reference": 1,
                "account_number": "NL90ABNA0585647886",
                "description": "string",
                "start_balance": 1,
                "mutation": "+1.0",
                "end_balance": 3
            },
            {
                "reference": 2,
                "account_number": "NL90ABNA0585647886",
                "description": "string",
                "start_balance": 1,
                "mutation": "+1.0",
                "end_balance": 2
            }
        ]

        response = client.post(self.url, json=data)
        body = response.json()

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(body['valid_transactions']), 1)
        self.assertEqual(len(body['invalid_transactions']), 1)
        self.assertEqual(len(body['raw_transactions']), 2)
