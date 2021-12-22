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
                purpleair(dbadapter=db, url_template=os.environ['purpleair_url'])
            elif personality == 'atmotube':
                atmotube(dbadapter=db, url_template=os.environ['atmotube_url'])
            elif personality == 'thingspeak':
                thingspeak(dbadapter=db, url_template=os.environ['thingspeak_url'])
            elif personality == 'geonames':
                fact = GeonamesFactory(personality=personality, options=args[1:])
                geonames(country_data_dir=fact.country_data_dir, include=fact.country_to_include, dbadapter=db,
                         patient_poscodes_dir=fact.patient_poscode_dir)
            else:
                raise ValueError(f"Wrong command line argument '{personality}'")
        print(f"\ndatabase connection closed successfully")
    except (HTTPError, ValueError, KeyError) as err:
        print(f"{err!r} exception caught in {main.__name__}")
        sys.exit(1)
    finally:
        stop = perf_counter()
        print(f"elapsed: {stop - start}s")
