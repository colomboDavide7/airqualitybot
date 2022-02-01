# ======================================
# @author:  Davide Colombo
# @date:    2022-02-1, mar, 20:39
# ======================================
from datetime import datetime


def sqlize(iterable) -> str:
    return "(" + ','.join(_safe_sqlize_item(item) if item is not None else 'NULL' for item in iterable) + ")"


def _safe_sqlize_item(item) -> str:
    if isinstance(item, datetime) or \
       isinstance(item, str):
        return f"'{item}'"
    elif isinstance(item, (float, int)):
        return str(item)
    else:
        raise ValueError(f"Cannot sqlize item = '{item}'")
