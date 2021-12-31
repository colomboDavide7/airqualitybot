######################################################
#
# Author: Davide Colombo
# Date: 31/12/21 08:10
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
# from os import environ
# from dotenv import load_dotenv
# # from airquality.add_fixed_sensors import AddFixedSensors
# from airquality.database_gateway import DatabaseGateway
# from airquality.database_adapter import Psycopg2Adapter
# # from airquality.datamodel_builder import PurpleairDatamodelBuilder
# from airquality.add_mobile_measures import AddMobileMeasures
# from airquality.timeiter_url import AtmotubeTimeIterableURL
# from airquality.datamodel_builder import AtmotubeDatamodelBuilder
#
#
# def main():
#     load_dotenv(dotenv_path='.env')
#     dbadapter = Psycopg2Adapter(
#         dbname=environ['dbname'], user=environ['user'], password=environ['password'], host=environ['host'],
#         port=environ['port']
#     )
#     output_gateway = DatabaseGateway(dbadapter=dbadapter)

    # url_template = environ['atmotube_url']
    # code2id = output_gateway.get_measure_param_owned_by(owner="atmotube")
    # apiparam = output_gateway.get_apiparam_of_type(sensor_type="atmotube")
    # print(repr(apiparam))
    #
    # for param in apiparam:
    #     url = url_template.format(api_key=param.api_key, api_id=param.api_id, api_fmt="json")
    #     urls = AtmotubeTimeIterableURL(url=url, begin=param.last_acquisition)
    #
    #     for url in urls:
    #         AddMobileMeasures(
    #             output_gateway=output_gateway,
    #             start_packet_id=output_gateway.get_max_mobile_packet_id_plus_one(),
    #             filter_ts=output_gateway.get_last_acquisition_of_sensor_channel(sensor_id=param.sensor_id,
    #                                                                             ch_name=param.ch_name),
    #             code2id=code2id,
    #             sensor_id=param.sensor_id,
    #             ch_name=param.ch_name
    #         ).process(datamodels=AtmotubeDatamodelBuilder(url=url))

    # existing_names = output_gateway.get_existing_sensor_names_of_type(sensor_type='purpleair')
    # start_sensor_id = output_gateway.get_start_sensor_id()
    # use_case = AddFixedSensors(output_gateway=output_gateway, existing_names=existing_names, start_sensor_id=start_sensor_id)
    #
    # datamodels = PurpleairDatamodelBuilder(url=environ['purpleair_url'])
    # use_case.process(datamodels=datamodels)
    # print('success')
