# noqa: D100
from oembedpy import providers


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
    provider = providers.Provider.parse_obj(RAW["23HQ"])
    assert provider.name == "23HQ"
    assert provider.endpoints[0].url == "http://www.23hq.com/23/oembed"


class TestForProviderRepository:  # noqa: D101
    def test__not_find(self):  # noqa: D102
        repo = providers.EndpointRepository([])
        assert repo.find("http://example.com") is None

    def test__find(self):  # noqa: D102
        provider = providers.Provider.parse_obj(RAW["23HQ"])
        repo = providers.EndpointRepository([provider])
        endpoint = repo.find("http://www.23hq.com/mprove/photo/111654186")
        assert endpoint is not None
