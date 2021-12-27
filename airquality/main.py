######################################################
#
# Author: Davide Colombo
# Date: 16/12/21 09:35
# Description: Restart from scratch
#
######################################################
from airquality.atmotube import atmotube
from airquality.purpleair import purpleair
from airquality.thingspeak import thingspeak
from airquality.geonames import geonames
from airquality.open_weather_map import openweathermap
from airquality.program_handler import ProgramHandler
from airquality.program_timer import ProgramTimer
from airquality.dbadapter import Psycopg2DBAdapter
from airquality.geonames_factory import GeonamesFactory
from airquality.purpleair_factory import PurpleairFactory
from airquality.measure_factory import AtmotubeFactory, ThingspeakFactory
from airquality.open_weather_map_factory import OpenWeatherMapFactory


def main():

    with ProgramHandler() as handler:
        with ProgramTimer():
            personality = handler.personality
            options = handler.options

            psycopg2adapter = Psycopg2DBAdapter(
                dbname=handler.dbname, host=handler.host, port=handler.port, user=handler.user, password=handler.password
            )
            with psycopg2adapter as dbadapter:
                if personality == 'purpleair':
                    fact = PurpleairFactory(personality=personality, dbadapter=dbadapter, options=options)
                    purpleair(sensor_dict=fact.sensor_dict, apiparam_dict=fact.apiparam_dict, geolocation_dict=fact.geolocation_dict, url_template=fact.url_template)
                if personality == 'atmotube':
                    fact = AtmotubeFactory(personality=personality, dbadapter=dbadapter, options=options)
                    atmotube(mobile_dict=fact.measure_dict, measure_param_dict=fact.measure_param_dict, apiparam_dict=fact.apiparam_dict, url_template=fact.url_template)
                if personality == 'thingspeak':
                    fact = ThingspeakFactory(personality=personality, dbadapter=dbadapter, options=options)
                    thingspeak(measure_dict=fact.measure_dict, measure_param_dict=fact.measure_param_dict, apiparam_dict=fact.apiparam_dict, url_template=fact.url_template)
                if personality == 'geonames':
                    fact = GeonamesFactory(personality=personality, dbadapter=dbadapter, options=options)
                    geonames(geonames_dict=fact.geonames_dict, geoarea_dict=fact.geoarea_dict, service_dict=fact.service_dict, poscodes_files=fact.poscodes_files)
                if personality == 'openweathermap':
                    fact = OpenWeatherMapFactory(personality=personality, dbadapter=dbadapter, options=options)
                    openweathermap(service_apiparam=fact.service_api_param_dict, geoarea_dict=fact.geoarea_dict, url_template=fact.url_template)
