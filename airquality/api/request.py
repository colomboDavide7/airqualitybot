#################################################
#
# @Author: Davide Colombo
# @Date: mer, 20-10-2021, 08:09
# @Description: this script defines an to_delete class that wraps the 'urllib' module functionality for connecting
#               to sensor's API and fetch data.
#
#################################################
from urllib.request import urlopen
from urllib.error import URLError


def fetch_from_url(url: str) -> str:
    try:
        return urlopen(url).read()
    except URLError as err:
        raise SystemExit(f"{fetch_from_url.__name__}() catches a {err.__class__.__name__} error => {err!s}")
