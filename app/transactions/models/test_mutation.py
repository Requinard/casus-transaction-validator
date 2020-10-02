from decimal import Decimal
from unittest import TestCase

from .mutation import Mutation


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
