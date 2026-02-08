"""Command-line interface for bind-shell."""

import click
from simple_bind_shell.bind_shell import BindShell


@click.command()
@click.option(
    '--host', '-h',
    default='0.0.0.0',
    help='Host address to bind to'
)
@click.option(
    '--port', '-p',
    default=4444,
    type=int,
    help='Port to listen on'
)
@click.option(
    '--max-connections', '-m',
    default=4,
    type=int,
    help='Maximum number of queued connections'
)
@click.version_option()
def main(host, port, max_connections):
    """Bind Shell - A lightweight bind shell server."""
    shell = BindShell(host=host, port=port, max_connections=max_connections)
    shell.start()


if __name__ == '__main__':
    main()
