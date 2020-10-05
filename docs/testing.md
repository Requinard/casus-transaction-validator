# Testing

## unit tests

I apply unittests to test isolated functions for my models.

The unittest library also runs a component test on the FastAPI app, by calling the internal HTTP endpoint with data. This can be compared to an integration test.

I do not run any tests for operations.py as they are only used to encapsulate real functionality that is in models.
