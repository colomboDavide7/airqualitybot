######################################################
#
# Author: Davide Colombo
# Date: 16/12/21 09:35
# Description: Restart from scratch
#
######################################################
import sys
import psycopg2
from time import perf_counter
from psycopg2.errors import Error
from urllib.error import HTTPError
from airquality.atmotube import atmotube
from airquality.purpleair import purpleair
from airquality.thingspeak import thingspeak


def main():
    args = sys.argv[1:]
    if len(args) != 1:
        print("USAGE => python(version) -m airquality [purpleair|atmotube|thingspeak]")
        sys.exit(1)

    personality = args[0]
    start = perf_counter()
    try:
        if personality == 'purpleair':
            purpleair()
        elif personality == 'atmotube':
            atmotube()
        elif personality == 'thingspeak':
            thingspeak()
        else:
            raise ValueError(f"Wrong command line argument '{personality}'")
    except (HTTPError, ValueError, KeyError, psycopg2.errors.Error) as err:
        print(f"{err!r} exception caught in {main.__name__}")
        sys.exit(1)

    stop = perf_counter()
    print(f"success in {stop - start} seconds")
