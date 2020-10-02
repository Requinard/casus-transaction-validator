from decimal import Decimal

from pydantic import PositiveInt


class Mutation(str):
    """
    Validate a mutation field.

    A mutation field starts with + or - and is followed by a decimal
    """

    def _get_sign(self):
        """
        Parses the first character into an allowed sign
        """

        if str(self)[0] == "-":
            return Decimal(-1)
        elif str(self)[0] == "+":
            return Decimal(1)

        raise ValueError("Unknown sign in mutation")

    def _get_number(self):
        """
        Parses the rest of the mutation into a Decimal
        """
        return Decimal(str(self)[1:])

    def _get_mutation_amount(self):
        """
        Combine the sign with the number to get if this returns a positive or negative mutation
        """
        return self._get_sign() * self._get_number()

    def validate_transaction(self, start_balance: Decimal, end_balance: Decimal, reference: PositiveInt):
        if start_balance + self._get_mutation_amount() != end_balance:
            raise ValueError(f"Transaction {reference} does not add up")

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            examples=['-1.0', '+1.0', '-1.20'],
        )

    @classmethod
    def validate(cls, v):
        if v[0] not in ["+", "-"]:
            raise TypeError("First character of a mutation must be + or -")

        try:
            Decimal(v[1:])
        except:
            raise TypeError("All other characters must be parsable to a decimal")

        return v

    class Config:
        allow_population_by_field_name = True
