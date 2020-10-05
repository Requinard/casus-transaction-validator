from pathlib import Path

import typer

from transactions.models import AcceptedContentTypes
from transactions.operations import load_file, parse_and_process

app = typer.Typer()


@app.command()
def process_file(p: Path = typer.Argument(..., exists=True, file_okay=True, readable=True)):
    try:
        content_type = AcceptedContentTypes.guess(p)
    except Exception:
        typer.echo("This content type is not accepted")
        raise typer.Exit(1)

    with open(p, 'rb') as f:
        rows_raw = load_file(content_type, f)

        collection = parse_and_process(rows_raw, content_type)

    typer.echo(f"Transactions found:\t{len(collection.raw_transactions)}")
    typer.echo(f"Invalid transactions:\t{len(collection.invalid_transactions)}")
    typer.echo(f"Valid transactions:\t{len(collection.valid_transactions)}")

    typer.echo("Showing transaction errors")

    for invalid_transaction in collection.invalid_transactions:
        [transaction, error] = invalid_transaction
        typer.echo(f"{error}\t-\t{transaction}")
