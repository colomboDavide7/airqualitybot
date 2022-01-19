# ======================================
# @author:  Davide Colombo
# @date:    2022-01-18, mar, 19:42
# ======================================
import logging
import requests
import requests.exceptions

MAX_SERVER_RESPONSE_TIMEOUT = 10.0


class BadAPIServerResponseError(Exception):
    """
    A subclass of Exception that is raised to signal that the communication with the API server failed.
    """
    pass


class APIServerWrapper(object):
    """
    A class that wraps the business logic for the communications between client (the machine) and the server
    by using the *requests* module.

    Keyword arguments:
        *url*               the url to fetch the data from.
        *timeout*           the amount of time to wait the server data before giving up.

    Raises:
        *BadAPIServerResponseError*         in case of any exception occurs during the communication with the server.

    """

    def __init__(self, timeout=MAX_SERVER_RESPONSE_TIMEOUT):
        self._timeout = timeout
        self._logger = logging.getLogger(__name__)

    def json(self, url: str):
        return self._safe_get(url).json()

    def _safe_get(self, url: str):
        try:
            return requests.get(url, timeout=self._timeout, headers={'Connection': 'close'})
        except requests.exceptions.HTTPError as err:
            self._logger.exception(repr(err))
            raise BadAPIServerResponseError(repr(err)) from None

    def __repr__(self):
        return f"{type(self).__name__}(timeout={self._timeout})"
