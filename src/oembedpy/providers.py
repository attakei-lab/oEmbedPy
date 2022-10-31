"""Providers handler."""
from dataclasses import dataclass, field
from fnmatch import fnmatch
from typing import Dict, List, Optional

import httpx


DEFAULT_PROVIDERS = "https://oembed.com/providers.json"


@dataclass
class Endpoint:
    """Provider endpoint."""

    schemes: List[str]
    url: str
    docs_url: Optional[str] = None
    example_urls: List[str] = field(default_factory=list)
    discovery: Optional[bool] = True
    formats: List[str] = field(default_factory=list)
    notes: Optional[str] = None


@dataclass
class Provider:
    """Structure of provider.

    this is implemented referred to `oEmbed repo`_.

    .. _oEmbed repo: https://github.com/iamcal/oembed/tree/master/providers
    """

    name: str
    url: str
    endpoints: List[Endpoint]

    @classmethod
    def parse_obj(cls, raw: dict) -> "Provider":
        """Parse dict object and create instance."""
        name = raw["provider_name"]
        url = raw["provider_url"]
        endpoints = [Endpoint(**e) for e in raw["endpoints"]]
        return cls(name=name, url=url, endpoints=endpoints)


class EndpointRepository:
    """Collection of endpoints for oEmbed providers."""

    def __init__(self, providers: List[Provider]):  # noqa: D107
        self._endpoints: Dict[str, Provider] = {}
        for provider in providers:
            self.register_provider(provider)

    def register_provider(self, provider: Provider):
        """Register endpoints from provider."""
        for endpoint in provider.endpoints:
            self._endpoints.update({s: endpoint for s in endpoint.schemes})

    def find(self, url: str) -> Optional[Endpoint]:
        """Find provider matched scheme for target URL.

        :params url: Content URL
        :returns: Matched provider object or None
        """
        for scheme, endpoint in self._endpoints.items():
            if fnmatch(url, scheme):
                return endpoint
        return None


def configure_repository(url: str = DEFAULT_PROVIDERS) -> EndpointRepository:
    """Create endpoint-repository bundled from oembed.com providers."""
    resp = httpx.get(url)
    repo = EndpointRepository([])
    for provider in resp.json():
        try:
            provider_ = Provider.parse_obj(provider)
            repo.register_provider(provider_)
        except TypeError:
            # TODO: Logging
            pass
    return repo
