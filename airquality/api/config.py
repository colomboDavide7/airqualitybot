######################################################
#
# Author: Davide Colombo
# Date: 18/11/21 19:22
# Description: INSERT HERE THE DESCRIPTION
#
######################################################

# This file contains the constants used for encoding and decoding the sensor data build by the APIExtractor class


FIELDS = 'fields'
FIELD_NAME = 'field_name'
FIELD_VALUE = 'field_value'

THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1A = {"field1": "pm1.0_atm_a", "field2": "pm2.5_atm_a",
                                             "field3": "pm10.0_atm_a", "field6": "temperature_a",
                                             "field7": "humidity_a"}
THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_1B = {"field1": "pm1.0_atm_b", "field2": "pm2.5_atm_b",
                                             "field3": "pm10.0_atm_b", "field6": "pressure_b"}
THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2A = {"field1": "0.3_um_count_a", "field2": "0.5_um_count_a",
                                             "field3": "1.0_um_count_a", "field4": "2.5_um_count_a",
                                             "field5": "5.0_um_count_a", "field6": "10.0_um_count_a"}
THINGSPEAK2DATABASE_PARAM_NAME_MAPPING_2B = {"field1": "0.3_um_count_b", "field2": "0.5_um_count_b",
                                             "field3": "1.0_um_count_b", "field4": "2.5_um_count_b",
                                             "field5": "5.0_um_count_b", "field6": "10.0_um_count_b"}