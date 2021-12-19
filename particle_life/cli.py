"""Console script for particle_life."""
import sys

import click
import main as particlelife


@click.command()
def main(args=None):
    """Console script for particle_life."""
    click.echo(
        "Replace this message by putting your code into " "particle_life.cli.main"
    )
    click.echo("See click documentation at https://click.palletsprojects.com/")

    particlelife.main()
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
