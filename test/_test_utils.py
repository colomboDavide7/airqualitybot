# ======================================
# @author:  Davide Colombo
# @date:    2022-01-18, mar, 20:36
# ======================================
import json


def get_json_response_from_file(filename: str):
    with open(f'test_resources/{filename}', 'r') as f:
        return json.load(f)
