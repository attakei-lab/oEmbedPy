# noqa: D100
from oembedpy import discovery


def test_find_refs__body_json_only():  # noqa: D103
    url = "https://speakerdeck.com/attakei/converting-pure-rest-to-revealjs"
    consumer_req = discovery.ConsumerRequest(
        endpoint="https://speakerdeck.com/oembed.json",
        url=url,
    )
    result = discovery.find_refs(url)
    assert len(result) == 1
    assert "json" in result
    assert result["json"] == consumer_req


def test_find_refs__body_json_and_xml():  # noqa: D103
    url = "https://www.youtube.com/watch?v=Y18v-HsxEAU"
    result = discovery.find_refs(url)
    assert len(result) == 2
    assert "json" in result
    assert "xml" in result
