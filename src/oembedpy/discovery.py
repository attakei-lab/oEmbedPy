"""Discovery funcs."""
from dataclasses import dataclass
from typing import Dict, Optional, Union
from urllib.parse import parse_qs, urlparse

import httpx
from bs4 import BeautifulSoup

Number = Union[float, int]


OEMBED_MIME_TYPES = {
    "application/json+oembed": "json",
    "text/xml+oembed": "xml",
}


@dataclass
class ConsumerRequest:
    """Parameter set for consumer-request."""

    endpoint: str
    content_url: str
    maxwidth: Optional[Number] = None
    maxheight: Optional[Number] = None
    format: Optional[str] = None

    @classmethod
    def from_url(cls, url: str) -> "ConsumerRequest":
        """Create object from full URL to provider API."""
        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        return cls(
            endpoint=f"{parsed.scheme}://{parsed.hostname}{parsed.path}",
            content_url=qs["url"][0],
        )


def find_refs(content_url: str) -> Dict[str, ConsumerRequest]:
    """Discover URLs of provider from content.

    :param content_url: URL of content.
    :returns: oEmbed resource URLs with format as key.
    """
    resources = {}
    resp = httpx.get(content_url)
    # Parse response header
    for key, val in resp.headers.multi_items():
        print(key, val)
        if key.lower() != "link":
            continue
        values = val.split("; ")
        if len(values) == 1:
            continue
        meta = dict(v.split("=") for v in values[1:])
        meta = {k: v[1:-1] for k, v in meta.items()}
        if "rel" not in meta or meta["rel"] != "alternate":
            continue
        if "type" not in meta or meta["type"] not in OEMBED_MIME_TYPES:
            continue
        resources[OEMBED_MIME_TYPES[meta["type"]]] = ConsumerRequest.from_url(
            values[0][1:-1]
        )
    # Parse response body
    soup = BeautifulSoup(resp.content, "html.parser")
    attrs = {
        "rel": "alternate",
        "type": lambda v: v in OEMBED_MIME_TYPES,
    }
    for elm in soup.find_all("link", attrs):
        resources[OEMBED_MIME_TYPES[elm["type"]]] = ConsumerRequest.from_url(
            elm["href"]
        )
    return resources
