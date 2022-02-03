# ======================================
# @author:  Davide Colombo
# @date:    2022-02-1, mar, 20:39
# ======================================
from typing import List


def sqlize_obj(self, attributes: List, header="", teardown="") -> str:
    header = header.strip('(, ')
    if header and header[-1] != ',':
        header += ','
    header = '(' + header

    teardown = teardown.strip(', )')
    if teardown and teardown[0] != ',':
        teardown = ',' + teardown
    teardown += ')'

    return header + \
           ','.join(_safe_sqlize_item(getattr(self, attr)) for attr in attributes) + \
           teardown


def sqlize_iterable(iterable) -> str:
    """
    A function that takes an iterable (tuple, list, set, ...) and properly converts its items into strings
    compatible with SQL database syntax.

    :param iterable:                the iterable object to convert into a SQL value
    :return:                        the SQL value corresponding to the iterable.
    """

    return "(" + ','.join(_safe_sqlize_item(item) for item in iterable) + ")"


def _safe_sqlize_item(item) -> str:
    if isinstance(item, (float, int)):
        return str(item)
    return f"'{item}'" if item is not None else 'NULL'
