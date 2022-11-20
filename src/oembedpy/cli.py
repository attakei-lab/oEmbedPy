"""Entrypoint of CLI tools."""
import sys

import click
import httpx
from oembedpy.providers import configure_repository


@click.command
@click.argument("url")
def main(url: str):  # noqa: D403
    """oEmbed consumer client."""
    if not url.startswith("http://") and not url.startswith("https://"):
        click.echo(err=True, message="URL must be started http:// or https://")
        sys.exit(1)
    repo = configure_repository()
    endpoint = repo.find(url)
    if not endpoint:
        click.echo(err=True, message="Provider is not found.")
        sys.exit(1)
    try:
        resp = httpx.get(endpoint.url, params={"url": url})
        resp.raise_for_status()
    except httpx.HTTPError as err:
        click.echo(err=True, message=f"Requesting for provider is failure: {err}")
        sys.exit(1)
    print(resp.content.decode())


if __name__ == "__main__":
    main()
