# ======================================
# @author:  Davide Colombo
# @date:    2022-02-3, gio, 14:55
# ======================================
from typing import List


def string_cleaner(s: str, char2remove: List[str]) -> str:
    return ''.join([c for c in s.lower() if c not in char2remove])


def literalize_number(number: float) -> str:
    number = "%.5f" % number
    return number.replace('.', 'dot').replace('-', 'minus')
