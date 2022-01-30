# ======================================
# @author:  Davide Colombo
# @date:    2022-01-18, mar, 19:42
# ======================================
import json
import requests
from typing import Dict
import requests.exceptions

_DEFAULT_TIMEOUT = 10.0
_DEFAULT_HEADERS = {'Connection': 'close'}
_DEFAULT_ERROR_MESSAGE = "unavailable"
_HTTP_ERROR_MESSAGES = {
    400: 'BAD REQUEST: the server could not understand the request due to invalid syntax.',
    401: 'UNAUTHORIZED: the client must authenticate itself to get the requested response.',
    403: 'FORBIDDEN: the client does not have access rights to the content (but it was successfully identified).',
    404: 'NOT FOUND: the server cannot find the requested resource',
    406: 'NOT ACCEPTABLE: the server does not find any content that conforms to the criteria given by the user agent',
    426: 'UPGRADE REQUIRED: the server refuses to perform the request using the current protocol.',
    429: 'TOO MANY REQUESTS: the user has sent too many requests in a given amount of time.',
    500: 'INTERNAL SERVER ERROR: the server has encountered a situation t does not know how to handle.',
    503: 'SERVICE UNAVAILABLE: the server is not ready to handle the request.',
    505: 'HTTP VERSION NOT SUPPORTED: the HTTP version used in the request is not supported by the server.',
    511: 'NETWORK AUTHENTICATION REQUIRED: the client need to authenticate to gain network access.'
}


def json_http_response(url: str, timeout=_DEFAULT_TIMEOUT, headers=None) -> Dict:
    if headers is None:
        headers = _DEFAULT_HEADERS
    http_response = _http_response(url=url, timeout=timeout, headers=headers)
    return json.loads(http_response.content)


def _http_response(url: str, timeout: float, headers: Dict) -> requests.Response:
    http_response = requests.get(
        url=url,
        timeout=timeout,
        headers=headers
    )
    return _verify_response_status(http_response)


def _verify_response_status(http_response: requests.Response) -> requests.Response:
    if 400 <= http_response.status_code < 600:
        content = http_response.content
        cause = _format_url_read_error(
            err_url=http_response.url,
            status_code=http_response.status_code,
            code_explain=_HTTP_ERROR_MESSAGES.get(http_response.status_code, _DEFAULT_ERROR_MESSAGE),
            http_jresp=json.loads(content) if content is not None else ""
        )
        raise requests.HTTPError(cause)
    return http_response


def _format_url_read_error(
    err_url: str,                       # The URL that causes the error.
    status_code: int,                   # The HTTP response status code.
    code_explain: str,                  # The HTTP status code text explanation.
    http_jresp: str                     # The HTTP response json representation.
):
    return f"[HTTP STATUS CODE]: {status_code} - " \
           f"[HTTP CODE EXPLANATION]: {code_explain} - " \
           f"[HTTP JSON RESPONSE]: {http_jresp} - " \
           f"[ERROR URL]: {err_url}"
