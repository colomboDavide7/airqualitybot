# ======================================
# @author:  Davide Colombo
# @date:    2022-01-18, mar, 19:42
# ======================================
_DEFAULT_TIMEOUT = 30.0
_DEFAULT_HEADERS = {'Connection': 'close'}

# ======================================
import requests
from typing import Dict
import requests.exceptions


def json_http_response(url: str, timeout=_DEFAULT_TIMEOUT, headers=None) -> Dict:
    if headers is None:
        headers = _DEFAULT_HEADERS
    http_response = requests.get(url=url, timeout=timeout, headers=headers)
    http_response.raise_for_status()
    if http_response.status_code != 204:
        return http_response.json()
    raise ValueError(f"[CODE]: 204 - [DESCRIPTION]: http response has not content - [URL]: {http_response.url}")
