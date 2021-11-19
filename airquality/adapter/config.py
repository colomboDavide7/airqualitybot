######################################################
#
# Author: Davide Colombo
# Date: 18/11/21 16:51
# Description: INSERT HERE THE DESCRIPTION
#
######################################################

# Insert all the variables used to map API sensor data to Database Record

# Sensor parameters
SENS_NAME = 'name'
SENS_TYPE = 'type'

# SensorInfo parameters
SENS_INFO = 'info'
SENS_CH = 'channel'

# Geolocation parameters
SENS_GEOM = 'geom'
SENS_LAT = 'lat'
SENS_LNG = 'lng'

# "Measure/API parameters" parameters
SENS_PARAM = 'par'
PAR_ID = 'par_id'
PAR_VAL = 'par_v'
PAR_NAME = 'par_n'

# Measurement parameter
REC_ID = 'record_id'

# Time parameter
TIMEST = 'ts'

# Dynamic make items
CLS = 'class'
KW = 'kwargs'

# Database-to-API constants used for decoding API parameters extracted from the database
CH_ID = 'channel_id'
CH_NAME = 'channel_name'
API_KEY = 'api_key'
MAC_ADDR = 'mac'

# Purpleair/Thingspeak sensor channels
FST_CH_A = "first channel A"
FST_CH_B = "first channel B"
SND_CH_A = "second channel A"
SND_CH_B = "second channel B"
CHANNEL_NAMES = [FST_CH_A, FST_CH_B, SND_CH_A, SND_CH_B]

# Atmotube channel name
ATMOTUBE_CHANNEL = "main"

# Purpleair/Thingspeak api parameters name. These names are used by the SensorAdapter for building the correct
# sensor packet that will be translated into SQL record by the APIParamRecord class. When these parameters are queried
# for fetching API data, ParamAdapter came in the game and uses them to get the correct channel parameters and build
# the URL.

# !!! THE VALUES CANNOT BE CHANGED BECAUSE THESE ARE THE NAMES OF THE PURPLEAIR 'fields' WITHIN THE API RESPONSE !!!

FST_ID_A = 'primary_id_a'
FST_KEY_A = 'primary_key_a'
FST_ID_B = 'primary_id_b'
FST_KEY_B = 'primary_key_b'
SND_ID_A = 'secondary_id_a'
SND_ID_B = 'secondary_id_b'
SND_KEY_A = 'secondary_key_a'
SND_KEY_B = 'secondary_key_b'

API_PARAM = [FST_ID_A, FST_ID_B, FST_KEY_A, FST_KEY_B, SND_ID_A, SND_ID_B, SND_KEY_A, SND_KEY_B]
