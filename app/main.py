import typer
import uvicorn

from transactions.commands import app as TransactionCommands

cli = typer.Typer()

cli.add_typer(TransactionCommands, name="transactions")


@cli.command()
def run(
    host: str = typer.Option("127.0.0.1"),
    port: int = typer.Option(8000),
    reload: bool = typer.Option(True)
):
    uvicorn.run("api:app", host=host, port=port, reload=reload)


if __name__ == '__main__':
    cli()
