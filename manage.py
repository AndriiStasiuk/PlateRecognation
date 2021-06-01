"""This module contains needed methods for correct service starting."""

import click

from image_gw_api.app import app
from image_gw_api.utils.logger import log


@click.group()
def command_group():
    """Init command group."""
    ...


@command_group.command()
@click.option("--host", default='127.0.0.1')
@click.option("--port", default=5000)
def runserver(host: str, port: str):
    """Setup params and run server.

    Args:
        host (str): Host where server will be running.
        port (str): Port where server will be running.

    """

    app.run(host=host, port=port)


if __name__ == "__main__":
    try:
        command_group()
    except Exception as error:
        log.critical(f"Error occurred: {error}")
        exit(1)
