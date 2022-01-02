######################################################
#
# Author: Davide Colombo
# Date: 01/01/22 10:57
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict
from airquality.datamodel.apiparam import APIParam
from airquality.database.gateway import DatabaseGateway
from airquality.url.timeiter_url import AtmotubeTimeIterableURL
from airquality.core.apidata_builder import AtmotubeAPIDataBuilder
from airquality.core.request_builder import AddAtmotubeMeasureRequestBuilder
from airquality.usecase.add_mobile_measures import AddMobileMeasures


class AddAtmotubeMeasuresRunner(object):
    """
    A *UsecaseRunner* that defines how to run the *AddMobileMeasures* UseCase.
    """

    def process_usecases(self, gateway: DatabaseGateway) -> None:
        code2id = gateway.get_measure_param_owned_by(owner=self.personality)
        apiparam = gateway.get_apiparam_of_type(sensor_type=self.personality)
        for param in apiparam:
            print(repr(param))
            for url in self.urls_of(param):
                start_packet_id = gateway.get_max_mobile_packet_id_plus_one()
                filter_ts = gateway.get_last_acquisition_of_sensor_channel(sensor_id=param.sensor_id, ch_name=param.ch_name)
                print(f"url='{url}', packet_id='{start_packet_id}', filter_ts='{filter_ts}'")
                AddMobileMeasures(
                    apiparam=param, filter_ts=filter_ts, gateway=gateway, start_packet_id=start_packet_id
                ).process(requests=self.requests_of(url=url, code2id=code2id))

    def urls_of(self, param: APIParam) -> AtmotubeTimeIterableURL:
        url_template = self.env.url_template(self.personality)
        pre_formatted_url = url_template.format(api_key=param.api_key, api_id=param.api_id, api_fmt="json")
        return AtmotubeTimeIterableURL(url=pre_formatted_url, begin=param.last_acquisition)

    def requests_of(self, url: str, code2id: Dict[str, int]) -> AddAtmotubeMeasureRequestBuilder:
        datamodels = AtmotubeAPIDataBuilder(url=url)
        return AddAtmotubeMeasureRequestBuilder(datamodel=datamodels, code2id=code2id)
