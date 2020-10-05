# Libraries

In this file I describe the library choices

## Pydantic

Pydantic is a library that offers constrained types for python. This means I can have automatic validation that a string fits a regex and such related properties.
This means I can use it for data ingestion and processing, as the assigned models will always be valid

https://pydantic-docs.helpmanual.io/

## FastAPI

FastAPI is a library to create web API's. It is integrated with pydantic and OpenAPI to offer automatic complex OpenAPI schema genertaion. 
The library also allows the automatic validation of input models and more

https://fastapi.tiangolo.com/

## Typer

Typer offer a small CLI library, in the same style as FastAPI. This makes CLI applications a breeze

https://typer.tiangolo.com/

## React

For the frontend app I picked react due to it's small footprint but massive capabilities. It follows a more functional paradigm compared to Angular and does not need as much setup

https://reactjs.org/
