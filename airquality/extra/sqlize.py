# ======================================
# @author:  Davide Colombo
# @date:    2022-02-1, mar, 20:39
# ======================================
from datetime import datetime


def sqlize(iterable) -> str:
    """
    A function that takes an iterable (tuple, list, set, ...) and properly converts its items into strings
    compatible with SQL database syntax.

    :param iterable:                the iterable object to convert into a SQL value
    :return:                        the SQL value corresponding to the iterable.
    """

    return "(" + ','.join(_safe_sqlize_item(item) if item is not None else 'NULL' for item in iterable) + ")"


def _safe_sqlize_item(item) -> str:
    if isinstance(item, (float, int)):
        return str(item)
    else:
        return f"'{item}'"
