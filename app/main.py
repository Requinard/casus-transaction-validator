import typer
import uvicorn

from api import app

cli = typer.Typer()


@cli.command()
def run(
    host: str = typer.Option("127.0.0.1"),
    port: int = typer.Option(8080),
    reload: bool = typer.Option(True)
):
    uvicorn.run(app, host=host, port=port, reload=reload)


if __name__ == '__main__':
    cli()
