######################################################
#
# Author: Davide Colombo
# Date: 01/01/22 16:53
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Dict
from datetime import datetime
from airquality.datamodel.apiparam import APIParam
from airquality.database.gateway import DatabaseGateway
from airquality.url.timeiter_url import ThingspeakTimeIterableURL
from airquality.core.apidata_builder import ThingspeakAPIDataBuilder
from airquality.core.request_builder import AddThingspeakMeasuresRequestBuilder
from airquality.core.request_validator import AddSensorMeasuresRequestValidator
from airquality.core.response_builder import AddStationMeasuresResponseBuilder


class AddThingspeakMeasures(object):
    """
    An *object* that defines the application UseCase of adding the measures detected by a fixed sensor (i.e., a station).

    Data are fetched from the API by building a set of urls by covering the period from the *last_acquisition* (queried
    from the database) to the moment of the application running.

    At each cycle, if there are new measures these are inserted into the database and the *last_acquisition* timestamp
    is updated to the timestamp of the last measure successfully inserted.
    """

    MAPPING_1A = {'field1': 'pm1.0_atm_a', 'field2': 'pm2.5_atm_a', 'field3': 'pm10.0_atm_a', 'field6': 'temperature_a',
                  'field7': 'humidity_a'}
    MAPPING_1B = {'field1': 'pm1.0_atm_b', 'field2': 'pm2.5_atm_b', 'field3': 'pm10.0_atm_b', 'field6': 'pressure_b'}
    MAPPING_2A = {'field1': '0.3_um_count_a', 'field2': '0.5_um_count_a', 'field3': '1.0_um_count_a',
                  'field4': '2.5_um_count_a', 'field5': '5.0_um_count_a', 'field6': '10.0_um_count_a'}
    MAPPING_2B = {'field1': '0.3_um_count_b', 'field2': '0.5_um_count_b', 'field3': '1.0_um_count_b',
                  'field4': '2.5_um_count_b', 'field5': '5.0_um_count_b', 'field6': '10.0_um_count_b'}
    FIELD_MAP = {'1A': MAPPING_1A, '1B': MAPPING_1B, '2A': MAPPING_2A, '2B': MAPPING_2B}

    def __init__(self, output_gateway: DatabaseGateway, input_url_template: str):
        self.output_gateway = output_gateway
        self.input_url_template = input_url_template

    @property
    def measure_param(self) -> Dict[str, int]:
        return self.output_gateway.get_measure_param_owned_by(owner="thingspeak")

    @property
    def api_param(self) -> List[APIParam]:
        return self.output_gateway.get_apiparam_of_type(sensor_type="thingspeak")

    @property
    def start_packet_id(self) -> int:
        return self.output_gateway.get_max_station_packet_id_plus_one()

    def fields_of(self, param: APIParam) -> Dict[str, str]:
        return self.FIELD_MAP[param.ch_name]

    def filter_ts_of(self, param: APIParam) -> datetime:
        return self.output_gateway.get_last_acquisition_of_sensor_channel(sensor_id=param.sensor_id, ch_name=param.ch_name)

    def urls_of(self, param: APIParam) -> ThingspeakTimeIterableURL:
        pre_formatted_url = self.input_url_template.format(api_key=param.api_key, api_id=param.api_id, api_fmt="json")
        return ThingspeakTimeIterableURL(url=pre_formatted_url, begin=param.last_acquisition, step_size_in_days=7)

    def run(self) -> None:
        measure_param = self.measure_param
        for param in self.api_param:
            print(repr(param))
            for url in self.urls_of(param):
                datamodel_builder = ThingspeakAPIDataBuilder(url=url)
                print(f"found #{len(datamodel_builder)} API data")

                request_builder = AddThingspeakMeasuresRequestBuilder(
                    datamodel=datamodel_builder, code2id=measure_param, field_map=self.fields_of(param)
                )
                print(f"found #{len(request_builder)} requests")

                validator = AddSensorMeasuresRequestValidator(request=request_builder, filter_ts=self.filter_ts_of(param))
                print(f"found #{len(validator)} valid requests")

                response_builder = AddStationMeasuresResponseBuilder(
                    requests=validator, start_packet_id=self.start_packet_id, sensor_id=param.sensor_id
                )
                print(f"found #{len(response_builder)} responses")

                if len(response_builder) > 0:
                    print(f"found responses within [{validator[0].timestamp!s} - {validator[-1].timestamp!s}]")
                    self.output_gateway.insert_station_measures(responses=response_builder)
                    last_acquisition = validator[-1].timestamp.strftime("%Y-%m-%d %H:%M:%S")
                    self.output_gateway.update_last_acquisition(
                        timestamp=last_acquisition, sensor_id=param.sensor_id, ch_name=param.ch_name
                    )
