# Architecture

```
models
    |
operations
|       |
api     commands
```

In this app, I use an onion architecture with BDD. This means that the core of the project are my models and their relations.

All operations on models are pure. This means that they do not have side effects and do not throw any exceptions.

To access the models we use `operations`. These functions handle any side effects that might occur before we get to operations on the models.

This also detaches the application so we can serve our functionality via `api` and `commands`

`api` manages HTTP bindings and the OpenAPI schema. This means parsing inputs and doing anything related to HTTP operations.

`commands` contains CLI commands to call operations.

This is all taken from a functional-design aspect.
