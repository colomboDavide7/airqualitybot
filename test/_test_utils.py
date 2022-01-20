# ======================================
# @author:  Davide Colombo
# @date:    2022-01-18, mar, 20:36
# ======================================
import json
from timezonefinder import TimezoneFinder
from dateutil import tz
from datetime import tzinfo


def get_json_response_from_file(filename: str):
    with open(f'test_resources/{filename}', 'r') as f:
        return json.load(f)


def get_tzinfo_from_coordinates(latitude: float, longitude: float) -> tzinfo:
    tz_name = TimezoneFinder().timezone_at(lat=latitude, lng=longitude)
    return tz.gettz(tz_name)
