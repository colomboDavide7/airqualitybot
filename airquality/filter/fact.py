######################################################
#
# Author: Davide Colombo
# Date: 11/12/21 19:29
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.filter.namefilt as nameflt
import airquality.filter.geolocation as geoflt


def get_filter(command_name: str, command_type: str):

    if command_name == 'init':
        if command_type == 'purpleair':
            return nameflt.NameFilter()
    elif command_name == 'update':
        if command_type == 'purpleair':
            return geoflt.GeoFilter()
    else:
        raise SystemExit(f"{get_filter.__name__} work in progress...")
