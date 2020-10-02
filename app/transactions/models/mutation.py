from decimal import Decimal

from pydantic import PositiveInt


class Mutation(str):
    def _get_sign(self):
        """
        Gets the sign
        """

        if str(self)[0] == "-":
            return Decimal(-1)
        elif str(self)[0] == "+":
            return Decimal(1)

        raise ValueError("Unknown sign in mutation")

    def _get_number(self):
        return Decimal(str(self)[1:])

    def _get_mutation_amount(self):
        return self._get_sign() * self._get_number()

    # todo validate mutation
    def validate_transaction(self, start_balance: Decimal, end_balance: Decimal, reference: PositiveInt):
        if start_balance + self._get_mutation_amount() != end_balance:
            raise ValueError(f"Transaction {reference} does not add up")

    @classmethod
    def __get_validators__(cls):
        # one or more validators may be yielded which will be called in the
        # order to validate the input, each validator will receive as an input
        # the value returned from the previous validator
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        # __modify_schema__ should mutate the dict it receives in place,
        # the returned value will be ignored
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

    class Config:
        allow_population_by_field_name = True
