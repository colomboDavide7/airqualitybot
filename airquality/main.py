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
#
#
# def main():
#     pass
#
#     load_dotenv(dotenv_path='.env')
#     dbadapter = Psycopg2Adapter(
#         dbname=environ['dbname'], user=environ['user'], password=environ['password'], host=environ['host'], port=environ['port']
#     )
#     output_gateway = DatabaseGateway(dbadapter=dbadapter)

    # existing_names = output_gateway.get_existing_sensor_names_of_type(sensor_type='purpleair')
    # start_sensor_id = output_gateway.get_start_sensor_id()
    # use_case = AddFixedSensors(output_gateway=output_gateway, existing_names=existing_names, start_sensor_id=start_sensor_id)
    #
    # datamodels = PurpleairDatamodelBuilder(url=environ['purpleair_url'])
    # use_case.process(datamodels=datamodels)
    # print('success')
