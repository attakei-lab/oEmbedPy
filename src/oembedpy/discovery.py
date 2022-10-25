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
    url: str
    maxwidth: Optional[Number] = None
    maxheight: Optional[Number] = None
    format: Optional[str] = None


def find_refs(content_url: str) -> Dict[str, ConsumerRequest]:
    """Discover URLs of provider from content.

    :param content_url: URL of content.
    :returns: oEmbed resource URLs with format as key.
    """
    resources = {}
    resp = httpx.get(content_url)
    soup = BeautifulSoup(resp.content, "html.parser")
    attrs = {
        "rel": "alternate",
        "type": lambda v: v in OEMBED_MIME_TYPES,
    }
    for elm in soup.find_all("link", attrs):
        url = urlparse(elm["href"])
        qs = parse_qs(url.query)
        req = ConsumerRequest(
            endpoint=f"{url.scheme}://{url.hostname}{url.path}",
            url=qs["url"][0],
        )
        resources[OEMBED_MIME_TYPES[elm["type"]]] = req
    return resources
