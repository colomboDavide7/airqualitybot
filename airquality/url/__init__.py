# ======================================
# @author:  Davide Colombo
# @date:    2022-01-24, lun, 20:45
# @source:  https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
# ======================================

DEFAULT_ERROR_MESSAGE = "unavailable"

HTTP_ERROR_MESSAGES = {
    400: '400, BAD REQUEST: the server could not understand the request due to invalid syntax.',
    401: '401, UNAUTHORIZED: the client must authenticate itself to get the requested response.',
    403: '403, FORBIDDEN: the client does not have access rights to the content (but it was successfully identified).',
    404: '404, NOT FOUND: the server cannot find the requested resource',
    406: '406, NOT ACCEPTABLE: the server does not find any content that conforms to the criteria given by the user agent',
    426: '426, UPGRADE REQUIRED: the server refuses to perform the request using the current protocol.',
    429: '429, TOO MANY REQUESTS: the user has sent too many requests in a given amount of time.',
    500: '500, INTERNAL SERVER ERROR: the server has encountered a situation t does not know how to handle.',
    503: '503, SERVICE UNAVAILABLE: the server is not ready to handle the request.',
    505: '505, HTTP VERSION NOT SUPPORTED: the HTTP version used in the request is not supported by the server.',
    511: '511, NETWORK AUTHENTICATION REQUIRED: the client need to authenticate to gain network access.'
}
