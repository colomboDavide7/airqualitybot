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
