# ======================================
# @author:  Davide Colombo
# @date:    2022-02-2, mer, 11:12
# ======================================
from typing import Dict, Any, List


def nested_search_dict(source: Dict[str, Any], keywords: List[str]):
    """
    A function that searches the keywords into a dictionary. Each keyword is sequentially searched one level at a time.

    PRACTICAL EXAMPLE:

    Calling the function on source = {'k1': 'v1', 'k2': 'v2', 'k3': {'kk1': 'vv1', 'kk2': {'kkk1': 'vvv1'}}}
    by using a keyword path equal to ['k3', 'kk2', 'kkk1'], returns 'vvv1'

    """

    if type(source) != dict:
        return source
    return nested_search_dict(source=source[keywords.pop(0)], keywords=keywords)
