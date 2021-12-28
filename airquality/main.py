######################################################
#
# Author: Davide Colombo
# Date: 16/12/21 09:35
# Description: Restart from scratch
#
######################################################
import os
from airquality.atmotube import Atmotube
from airquality.thingspeak_cls import Thingspeak
from airquality.purpleair import Purpleair
from airquality.geonames import geonames
from airquality.open_weather_map import openweathermap
from airquality.env import Environment
from airquality.argshandler import ArgsHandler
from airquality.program_timer import ProgramTimer
from airquality.dbadapter import Psycopg2DBAdapter


def main():

    with Environment() as env:
        with ProgramTimer():

            args = ArgsHandler(valid_pers=env.valid_personalities, valid_options=env.valid_options)
            personality = args.personality
            options = args.options

            psycopg2adapter = Psycopg2DBAdapter(
                dbname=env.dbname, host=env.host, port=env.port, user=env.user, password=env.password
            )

            with psycopg2adapter as dbadapter:
                if personality == 'purpleair':
                    url = os.environ[f'{personality}_url']
                    Purpleair(personality=personality, url=url, dbadapter=dbadapter).execute()
                if personality == 'atmotube':
                    url = os.environ[f'{personality}_url']
                    url_opt = {'api_fmt': 'json'}
                    Atmotube(personality=personality, url_template=url, dbadapter=dbadapter, **url_opt).execute()

                # if personality == 'thingspeak':
                #     fact = ThingspeakFactory(personality=personality, dbadapter=dbadapter, options=options)
                #     Thingspeak(personality=personality, url_template=fact.url_template, **fact.url_options).execute()
                #     # thingspeak(measure_dict=fact.measure_dict, measure_param_dict=fact.measure_param_dict, apiparam_dict=fact.apiparam_dict, url_template=fact.url_template)
                # if personality == 'geonames':
                #     fact = GeonamesFactory(personality=personality, dbadapter=dbadapter, options=options)
                #     geonames(geonames_dict=fact.geonames_dict, geoarea_dict=fact.geoarea_dict, service_dict=fact.service_dict, poscodes_files=fact.poscodes_files)
                # if personality == 'openweathermap':
                #     fact = OpenWeatherMapFactory(personality=personality, dbadapter=dbadapter, options=options)
                #     openweathermap(service_apiparam=fact.service_api_param_dict, geoarea_dict=fact.geoarea_dict, measure_param_dict=fact.measure_param_dict, url_template=fact.url_template)
