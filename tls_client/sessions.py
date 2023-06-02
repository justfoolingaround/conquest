from .cffi import request, freeMemory
from .cookies import (
    cookiejar_from_dict,
    merge_cookies,
    extract_cookies_to_jar,
)

from .exceptions import TLSClientExeption
from .response import build_response
from .structures import CaseInsensitiveDict
from .__version__ import __version__
from .utils.tls_settings import Settings

from typing import Any, Optional, Union, Dict, List
import urllib.parse
import base64
import ctypes
import uuid

import orjson


DEFAULT_CLIENT_HEADERS = {
    "Accept": "*/*",
    "Connection": "keep-alive",
}

DEFAULT_CLIENT_HEADERS["User-Agent"] = f"tls-client/{__version__}"


class Session:
    def __init__(
        self,
        headers=DEFAULT_CLIENT_HEADERS,
        timeout: Optional[int] = None,
        proxies: Optional[Dict[str, str]] = None,
        *,
        encoding: str = "utf-8",
        settings: Optional[Settings] = None,
    ) -> None:
        self.timeout = timeout
        self.headers = CaseInsensitiveDict(headers)
        self.proxies = proxies

        self.encoding = encoding

        self.session_id = str(uuid.uuid4())
        self.cookies = cookiejar_from_dict({})

        self.tls_settings = settings or Settings()

    def execute_request(
        self,
        method: str,
        url: str,
        params: Optional[Dict[str, str]] = None,
        data: Optional[Union[str, dict, bytes, bytearray]] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        json: Optional[Union[Dict, List, str, bytes, bytearray]] = None,
        allow_redirects: bool = False,
        insecure_skip_verify: bool = False,
        timeout: Optional[int] = None,
        proxies: Optional[Union[Dict[str, str], str]] = None,
        settings: Optional[Settings] = None,
    ):
        if params is not None:
            url = f"{url}?{urllib.parse.urlencode(params, doseq=True)}"

        content_type = None
        request_body = None

        if data is None:
            if json is not None:
                content_type = "application/json"

                if isinstance(json, bytes):
                    request_body = json

                if isinstance(json, (dict, list)):
                    json = orjson.dumps(json)

                if isinstance(json, str):
                    request_body = json.encode(self.encoding)

                if isinstance(json, bytearray):
                    request_body = bytes(json)

                if not isinstance(json, (bytes, str, bytearray)):
                    raise ValueError(
                        "json must be either of: dict, list, bytes, str or bytearray"
                    )
        else:
            if isinstance(data, (dict, list)):
                request_body = urllib.parse.urlencode(data, doseq=True)
                content_type = "application/x-www-form-urlencoded"

            else:
                if isinstance(data, str):
                    request_body = data.encode(self.encoding)

                if isinstance(data, bytes):
                    request_body = data

                if isinstance(data, bytearray):
                    request_body = bytes(data)

                if not isinstance(data, (bytes, str, bytearray)):
                    raise ValueError(
                        "data must be either of: dict, list, bytes, str or bytearray"
                    )

        if headers is not None:
            request_headers = CaseInsensitiveDict(headers.copy())
        else:
            request_headers = CaseInsensitiveDict()

        if self.headers is not None:
            request_headers.update(self.headers)

        if content_type is not None and "content-type" not in request_headers:
            request_headers["Content-Type"] = content_type

        for header_key, header_value in request_headers.items():
            if header_value is None:
                del request_headers[header_key]

        request_jar = merge_cookies(self.cookies, cookies or {})

        request_cookies = list(
            map(
                lambda cookie: {
                    "domain": cookie.domain,
                    "expires": cookie.expires,
                    "name": cookie.name,
                    "path": cookie.path,
                    "value": cookie.value,
                },
                request_jar,
            )
        )

        scheme = urllib.parse.urlparse(url).scheme

        request_proxy = None

        if proxies is None:
            if self.proxies is not None:
                proxies = self.proxies

        if isinstance(proxies, dict):
            if scheme in proxies:
                request_proxy = proxies[scheme]
        else:
            request_proxy = proxies

        request_timeout = timeout or self.timeout

        is_byte_request = isinstance(request_body, bytes)

        request_payload = {
            "sessionId": self.session_id,
            "followRedirects": allow_redirects,
            "headers": dict(request_headers),
            "insecureSkipVerify": insecure_skip_verify,
            "isByteRequest": is_byte_request,
            "proxyUrl": request_proxy,
            "requestUrl": url,
            "requestMethod": method,
            "requestBody": base64.b64encode(request_body).decode()
            if is_byte_request
            else request_body,
            "requestCookies": request_cookies,
        }

        if request_timeout is not None:
            request_payload["timeoutSeconds"] = request_timeout

        settings_payload = (settings or self.tls_settings).get()
        request_payload.update(settings_payload)

        response = request(orjson.dumps(request_payload))
        response_bytes = ctypes.string_at(response)
        response_string = response_bytes.decode("utf-8")
        response_object = orjson.loads(response_string)
        freeMemory(response_object["id"].encode("utf-8"))

        if response_object["status"] == 0:
            raise TLSClientExeption(response_object["body"])

        response_cookie_jar = extract_cookies_to_jar(
            request_url=url,
            request_headers=request_headers,
            cookie_jar=request_jar,
            response_headers=response_object["headers"],
        )

        return build_response(
            response_object, response_cookie_jar, encoding=self.encoding
        )

    def get(self, url: str, **kwargs: Any):
        """Sends a GET request"""
        return self.execute_request(method="GET", url=url, **kwargs)

    def options(self, url: str, **kwargs: Any):
        """Sends a OPTIONS request"""
        return self.execute_request(method="OPTIONS", url=url, **kwargs)

    def head(self, url: str, **kwargs: Any):
        """Sends a HEAD request"""
        return self.execute_request(method="HEAD", url=url, **kwargs)

    def post(
        self,
        url: str,
        data: Optional[Union[str, dict, bytes, bytearray]] = None,
        json: Optional[Union[Dict, List]] = None,
        **kwargs: Any,
    ):
        """Sends a POST request"""
        return self.execute_request(
            method="POST", url=url, data=data, json=json, **kwargs
        )

    def put(
        self,
        url: str,
        data: Optional[Union[str, dict, bytes, bytearray]] = None,
        json: Optional[Union[Dict, List]] = None,
        **kwargs: Any,
    ):
        """Sends a PUT request"""
        return self.execute_request(
            method="PUT", url=url, data=data, json=json, **kwargs
        )

    def patch(
        self,
        url: str,
        data: Optional[Union[str, dict, bytes, bytearray]] = None,
        json: Optional[Union[Dict, List]] = None,
        **kwargs: Any,
    ):
        """Sends a PATCH request"""
        return self.execute_request(
            method="PATCH", url=url, data=data, json=json, **kwargs
        )

    def delete(self, url: str, **kwargs: Any):
        """Sends a DELETE request"""
        return self.execute_request(method="DELETE", url=url, **kwargs)
