from .cookies import RequestsCookieJar
from .structures import CaseInsensitiveDict


from typing import Dict
import orjson


class Response(object):
    def __init__(
        self,
        id: str,
        body: str,
        cookies: RequestsCookieJar,
        headers: CaseInsensitiveDict,
        session_id: str,
        status: int,
        target: str,
        protocol: str,
        *,
        encoding: str = "utf-8",
    ):
        self.id = id
        self.body = body
        self.cookies = cookies
        self.headers = headers
        self.session_id = session_id
        self.status_code = status
        self.url = target

        self.encoding = encoding
        self.protocol = protocol

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def __repr__(self):
        return f"<Response [{self.protocol} / {self.status_code}]>"

    def json(self, **kwargs):
        """parse response body to json (dict/list)"""
        return orjson.loads(self.body, **kwargs)

    @property
    def content(self):
        """Content of the response, in bytes."""

        return self.body.encode(self.encoding)

    @property
    def text(self):
        """Content of the response, in unicode."""
        return self.body


def build_response(
    response: Dict, res_cookies: RequestsCookieJar, encoding: str
) -> Response:
    """Builds a Response object"""

    return Response(
        id=response["id"],
        body=response["body"],
        cookies=res_cookies,
        headers=CaseInsensitiveDict(response["headers"]),
        session_id=response["sessionId"],
        status=response["status"],
        target=response["target"],
        protocol=response["usedProtocol"],
        encoding=encoding,
    )
