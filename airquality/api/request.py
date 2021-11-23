#################################################
#
# @Author: Davide Colombo
# @Date: mer, 20-10-2021, 08:09
# @Description: this script defines an adapter class that wraps the 'urllib' module functionality for connecting
#               to sensor's API and fetch data.
#
#################################################
import urllib.request as r
import urllib.error as e


def fetch_from_url(url: str) -> str:
    req = r.Request(url)
    try:
        return r.urlopen(req).read()
    except e.URLError as err:
        err_msg = f"'{fetch_from_url.__name__}()':"
        if hasattr(err, 'reason'):
            if err.reason == 'Bad Request':
                err_msg += f" bad URL => please check your parameters"
            else:
                err_msg += f" failed to reach the server => {err.reason}"
        elif hasattr(err, 'code'):
            err_msg = f"The server couldn't fulfill the request => error code={err.code}"

        raise SystemExit(err_msg)
