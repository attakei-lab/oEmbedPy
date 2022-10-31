# noqa: D100
import json

from pytest_httpserver import HTTPServer
from oembedpy import providers as t


RAW = {
    # Raw data from https://oembed.com/providers.json
    "23HQ": {
        "provider_name": "23HQ",
        "provider_url": "http://www.23hq.com",
        "endpoints": [
            {
                "schemes": ["http://www.23hq.com/*/photo/*"],
                "url": "http://www.23hq.com/23/oembed",
            }
        ],
    },
}


def test__Provider__parse_obj():  # noqa: D103
    provider = t.Provider.parse_obj(RAW["23HQ"])
    assert provider.name == "23HQ"
    assert provider.endpoints[0].url == "http://www.23hq.com/23/oembed"


class TestForProviderRepository:  # noqa: D101
    def test__not_find(self):  # noqa: D102
        repo = t.EndpointRepository([])
        assert repo.find("http://example.com") is None

    def test__find(self):  # noqa: D102
        provider = t.Provider.parse_obj(RAW["23HQ"])
        repo = t.EndpointRepository([provider])
        endpoint = repo.find("http://www.23hq.com/mprove/photo/111654186")
        assert endpoint is not None


def test__configure_repository(httpserver: HTTPServer):  # noqa: D103
    providers = [RAW["23HQ"]]
    httpserver.expect_request("/").respond_with_data(json.dumps(providers))
    repo = t.configure_repository(httpserver.url_for("/"))
    endpoint = repo.find("http://www.23hq.com/mprove/photo/111654186")
    assert endpoint is not None
