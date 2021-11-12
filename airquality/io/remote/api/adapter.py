#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 08:09
# @Description: this script defines an adapter class that wraps the 'urllib' module functionality for connecting
#               to sensor's API and fetch data.
#
#################################################
import urllib.request as r
import urllib.error as e


def fetch(url: str) -> str:
    req = r.Request(url)
    try:
        return r.urlopen(req).read()
    except e.URLError as err:
        if hasattr(err, 'reason'):
            err_msg = f"'{fetch.__name__}()': failed to reach the server => {err.reason}"
        elif hasattr(err, 'code'):
            err_msg = f"The server couldn't fulfill the {fetch.__name__} request => code={err.code}"
        else:
            err_msg = f"'{fetch.__name__}()': bad request => {err!s}"
        raise SystemExit(err_msg)
