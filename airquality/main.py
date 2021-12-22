######################################################
#
# Author: Davide Colombo
# Date: 16/12/21 09:35
# Description: Restart from scratch
#
######################################################
import os
import sys
import dotenv
from time import perf_counter
from urllib.error import HTTPError
from airquality.atmotube import atmotube
from airquality.purpleair import purpleair
from airquality.thingspeak import thingspeak
from airquality.geonames import geonames
from airquality.dbadapter import Psycopg2DBAdapter
from airquality.factory import GeonamesFactory
from airquality.purpleair_factory import PurpleairFactory
from airquality.atmotube_factory import AtmotubeFactory


def main():
    args = sys.argv[1:]
    if len(args) < 1:
        print("USAGE => python(version) -m airquality [purpleair|atmotube|thingspeak|geonames]")
        sys.exit(1)

    dotenv.load_dotenv(dotenv_path='.env')
    personality = args[0]
    start = perf_counter()
    try:
        db_adapter = Psycopg2DBAdapter(
            dbname=os.environ['database'],
            host=os.environ['host'],
            port=os.environ['port'],
            user=os.environ['user'],
            password=os.environ['password']
        )

        with db_adapter as db:
            print(f"database connection opened: {db!r}")
            if personality == 'purpleair':
                fact = PurpleairFactory(personality=personality, options=args[1:], dbadapter=db)
                purpleair(sensor_dict=fact.sensor_dict, apiparam_dict=fact.apiparam_dict, geolocation_dict=fact.geolocation_dict, url_template=fact.url_template)
            elif personality == 'atmotube':
                fact = AtmotubeFactory(personality=personality, options=args[1:], dbadapter=db)
                atmotube(mobile_dict=fact.mobile_dict, measure_param_dict=fact.measure_param_dict, apiparam_dict=fact.apiparam_dict, url_template=fact.url_template)
            elif personality == 'thingspeak':
                thingspeak(dbadapter=db, url_template=os.environ['thingspeak_url'])
            elif personality == 'geonames':
                fact = GeonamesFactory(personality=personality, options=args[1:], dbadapter=db)
                geonames(geonames_dict=fact.geonames_dict, geoarea_dict=fact.geoarea_dict, poscodes_files=fact.poscodes_files)
            else:
                raise ValueError(f"Wrong command line argument '{personality}'")
        print(f"\ndatabase connection closed successfully")
    except (HTTPError, ValueError, KeyError) as err:
        print(f"{err!r} exception caught in {main.__name__}")
        sys.exit(1)
    finally:
        stop = perf_counter()
        print(f"elapsed: {stop - start}s")
