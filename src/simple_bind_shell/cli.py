"""Command-line interface for bind-shell."""

import logging

import click

from simple_bind_shell.bind.bind_shell import (
    DEFAULT_CLIENT_TIMEOUT,
    DEFAULT_COMMAND_TIMEOUT,
    BindShell,
)
from simple_bind_shell.version import __version__


@click.command()
@click.option(
    "--host",
    "-h",
    default="0.0.0.0",
    envvar="BIND_SHELL_HOST",
    show_default=True,
    help="Host address to bind to",
)
@click.option(
    "--port",
    "-p",
    default=4444,
    type=click.IntRange(1, 65535),
    envvar="BIND_SHELL_PORT",
    show_default=True,
    help="Port to listen on",
)
@click.option(
    "--max-connections",
    "-m",
    default=4,
    type=click.IntRange(1, 100),
    envvar="BIND_SHELL_MAX_CONN",
    show_default=True,
    help="Maximum number of queued connections",
)
@click.option(
    "--command-timeout",
    default=DEFAULT_COMMAND_TIMEOUT,
    type=click.IntRange(1, 3600),
    envvar="BIND_SHELL_COMMAND_TIMEOUT",
    show_default=True,
    help="Per-command timeout in seconds",
)
@click.option(
    "--client-timeout",
    default=DEFAULT_CLIENT_TIMEOUT,
    type=click.IntRange(1, 86400),
    envvar="BIND_SHELL_CLIENT_TIMEOUT",
    show_default=True,
    help="Client idle timeout in seconds",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Enable verbose logging",
)
@click.version_option(version=__version__)
def main(host, port, max_connections, command_timeout, client_timeout, verbose):
    """Bind Shell - A lightweight bind shell server."""
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format=(
            "%(asctime)s - %(levelname)s - %(message)s" if verbose else "%(message)s"
        ),
    )
    shell = BindShell(
        host=host,
        port=port,
        max_connections=max_connections,
        command_timeout=command_timeout,
        client_timeout=client_timeout,
    )
    shell.start()


if __name__ == "__main__":
    main()
