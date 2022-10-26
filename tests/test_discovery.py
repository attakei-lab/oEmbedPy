# noqa: D100
from pytest_httpserver import HTTPServer
from oembedpy import discovery


def test_find_refs__body_json_only(httpserver: HTTPServer):  # noqa: D103
    httpserver.expect_request("/").respond_with_data(
        """
        <html>
            <head>
                <link
                    rel="alternate"
                    type="application/json+oembed"
                    href="http://example.com/oembed?url=http%3A%2F%2Fexample.com%2Fcontent"
                />
            </head>
        </html>
    """
    )
    consumer_req = discovery.ConsumerRequest(
        endpoint="http://example.com/oembed",
        url="http://example.com/content",
    )
    result = discovery.find_refs(httpserver.url_for("/"))
    assert len(result) == 1
    assert "json" in result
    assert result["json"] == consumer_req


def test_find_refs__body_json_and_xml(httpserver: HTTPServer):  # noqa: D103
    httpserver.expect_request("/").respond_with_data(
        """
        <html>
            <head>
                <link
                    rel="alternate"
                    type="application/json+oembed"
                    href="http://example.com/oembed?url=http%3A%2F%2Fexample.com%2Fcontent&format=json"
                />
                <link
                    rel="alternate"
                    type="text/xml+oembed"
                    href="http://example.com/oembed?url=http%3A%2F%2Fexample.com%2Fcontent&format=xml"
                />
            </head>
        </html>
    """
    )
    result = discovery.find_refs(httpserver.url_for("/"))
    assert len(result) == 2
    assert "json" in result
    assert "xml" in result


def test_find_refs__herder(httpserver: HTTPServer):  # noqa: D103
    httpserver.expect_request("/").respond_with_data(
        "",
        headers={
            "Link": '<http://example.com/oembed?url=http%3A%2F%2Fexample.com%2Fcontent&format=json>; rel="alternate"; type="application/json+oembed"',  # noqa: E501
        },
    )
    result = discovery.find_refs(httpserver.url_for("/"))
    assert len(result) == 1
    assert "json" in result


def test_find_refs__multiple_herders(httpserver: HTTPServer):  # noqa: D103
    httpserver.expect_request("/").respond_with_data(
        "",
        headers=[
            (
                "Link",
                '<http://example.com/oembed?url=http%3A%2F%2Fexample.com%2Fcontent&format=json>; rel="alternate"; type="application/json+oembed"',  # noqa: E501
            ),
            (
                "Link",
                '<http://example.com/oembed?url=http%3A%2F%2Fexample.com%2Fcontent&format=xml>; rel="alternate"; type="text/xml+oembed"',  # noqa: E501
            ),
        ],
    )
    result = discovery.find_refs(httpserver.url_for("/"))
    assert len(result) == 2
