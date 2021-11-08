######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 08/11/21 16:25
# Description: INSERT HERE THE DESCRIPTION
#
######################################################

from typing import List

# IMPORT GLOBAL VARIABLE FROM FETCH MODULE
import airquality.constants.system_constants as sc


# IMPORT CLASSES FROM AIRQUALITY MODULE
from airquality.api.url_builder import URLBuilder
from airquality.adapter.universal_api_adapter import UniversalAPIAdapter
from airquality.container.sql_container import MobileMeasurementSQLContainer, StationMeasurementSQLContainer
from airquality.container.sql_container_factory import SQLContainerFactory
from airquality.geom.postgis_geometry import PostGISPoint
from airquality.adapter.geom_adapter import GeometryAdapterAtmotube
from airquality.adapter.measurement_adapter import MeasurementAdapterFactory, MeasurementAdapterAtmotube, \
    MeasurementAdapterThingspeak
from airquality.adapter.channel_adapter import ChannelAdapter
from airquality.container.fetch_container_factory import FetchContainerFactory
from airquality.container.fetch_container import ChannelContainer, ChannelContainerWithFormattableAddress
from airquality.database.db_conn_adapter import Psycopg2ConnectionAdapterFactory
from airquality.parser.db_answer_parser import DatabaseAnswerParser
from airquality.parser.datetime_parser import DatetimeParser
from airquality.picker.query_picker import QueryPicker
from airquality.api.urllib_adapter import UrllibAdapter
from airquality.picker.json_param_picker import JSONParamPicker
from airquality.picker.api_param_picker import APIParamPicker
from airquality.picker.resource_picker import ResourcePicker
from airquality.parser.file_parser import FileParserFactory

# IMPORT SHARED CONSTANTS
from airquality.constants.shared_constants import DEBUG_HEADER, INFO_HEADER, EXCEPTION_HEADER


class DateFetchBot:

    def __init__(self,
                 dbconn,
                 url_builder_class=URLBuilder,
                 universal_api_adapter_class=UniversalAPIAdapter):
        self.dbconn = dbconn
        self.url_builder_class = url_builder_class
        self.universal_api_adapter_class = universal_api_adapter_class

    def run(self,
            api_address: str,
            url_param: str,
            sensor_ids: List[int],
            select_apiparam_query: str):

        for sensor_id in sensor_ids:
            print(20 * "*" + f" {sensor_id} " + 20 * '*')

            ################################ SELECT API PARAM FROM DATABASE ################################
            query = select_apiparam_query.format(sensor_id=sensor_id)
            answer = self.dbconn.send(executable_sql_query=query)
            api_param = DatabaseAnswerParser.parse_key_val_answer(answer)

            if not api_param:
                raise SystemExit(f"{EXCEPTION_HEADER} {DateFetchBot.__name__} fetched API param but are empty.")

            ################################ UNIVERSAL API ADAPTER ################################
            universal_api_adapter = self.universal_api_adapter_class()
            universal_api_param = universal_api_adapter.adapt(api_param)

            if sc.DEBUG_MODE:
                print(20 * "=" + " UNIVERSAL API PARAMETERS " + 20 * '=')
                for api_param in universal_api_param:
                    print(30*"*")
                    for key, val in api_param.items():
                        print(f"{DEBUG_HEADER} {key}={val!s}")

        ################################ SAFELY CLOSE DATABASE CONNECTION ################################
        self.dbconn.close_conn()
