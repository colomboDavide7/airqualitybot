# ======================================
# @author:  Davide Colombo
# @date:    2022-01-28, ven, 11:27
# ======================================
import functools


def _concat(*args, **kwargs) -> str:
    arguments = ', '.join(repr(arg) for arg in args) + ', '
    arguments += ', '.join(f"{k}={v}" for k, v in kwargs.items())
    return arguments


def throw_on(sentinel_value, exc_type):
    """
    A decorator function that raises a specific exception when the calls to the wrapped function returns a value equal
    to the sentinel value.

    :param sentinel_value:              the value that triggers the exception to be raised.
    :param exc_type:                    the class of the exception to be raised.
    """

    def throw_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            value = func(*args, **kwargs)
            if value == sentinel_value:
                raise exc_type(
                    "[FUNCTION]: '%s' - [ARGUMENTS]: %s - [RETURN]: '%s'" %
                    (func.__name__, _concat(*args, **kwargs), value)
                )
            return value
        return wrapper
    return throw_decorator


# def catch(exc_type, logger_name: str, level_name='warning'):
#     """
#     A decorator function that catches a specific type of exceptions and logs it event.
#
#     :param exc_type:                    the class of the exception to be caught.
#     :param logger_name:                 the logger's name.
#     :param level_name:                  the name's of the logging level.
#     """
#
#     _logger = logging.getLogger(logger_name)
#
#     def catch_decorator(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             try:
#                 return func(*args, **kwargs)
#             except exc_type as caught:
#                 logging_method = getattr(_logger, level_name)
#                 logging_method(
#                     "[FUNCTION]: '%s' - [ARGUMENTS]: %s - [CAUGHT]: '%s'" %
#                     (func.__name__, _concat(*args, **kwargs), repr(caught))
#                 )
#         return wrapper
#     return catch_decorator


def get_at(index: int):
    """
    A decorator function that returns the item at the specific index from the return value of a function.
    The function must return an object that supports slicing.

    :param index:                       the target item index from the return value of the function.
    """

    def index_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)[index]
        return wrapper
    return index_decorator


def constructor_of(obj_type):
    """
    A decorator function that builds an instance of a given class from the output of the function.

    :param obj_type:                    the class object to be built.
    :return:                            a new instance of the given class.
    """

    def constructor_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return obj_type(func(*args, **kwargs))
        return wrapper
    return constructor_decorator


def dict_from_tuples(key_index: int):
    """
    A decorator function that builds a dict object from a tuple of two items.

    :param key_index:                   the index of the item to be used as a key (must be one of 0 or 1).
    :return:                            a dict object which key items are those in position *key_index* within the tuple
    """

    if 1 < key_index < 0:
        raise IndexError(f"expected '{key_index}' to be 0 or 1")

    def dict_from_tuples_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return {t[key_index]: t[1-key_index] for t in func(*args, **kwargs)}
        return wrapper
    return dict_from_tuples_decorator
