# ======================================
# @author:  Davide Colombo
# @date:    2022-01-18, mar, 11:49
# ======================================

# ================================= #
#                                   #
# MEASURE PARAM TABLE
#                                   #
# ================================= #
SELECT_MEASURE_PARAM = "SELECT id, param_code FROM level0_raw.measure_param " \
                       "WHERE param_owner ILIKE '%{owner}%';"

# ================================= #
#                                   #
# SENSOR TABLE
#                                   #
# ================================= #
INSERT_SENSORS      = "INSERT INTO level0_raw.sensor VALUES {val};"
SELECT_MAX_SENS_ID  = "SELECT MAX(id) FROM level0_raw.sensor;"
SELECT_SENSOR_NAMES = "SELECT sensor_name FROM level0_raw.sensor WHERE sensor_type ILIKE '%{type}%';"

# ================================= #
#                                   #
# SENSOR AT LOCATION TABLE
#                                   #
# ================================= #
INSERT_SENSOR_LOCATION = "INSERT INTO level0_raw.sensor_at_location " \
                         "(sensor_id, valid_from, geom) VALUES {val};"

# ================================= #
#                                   #
# SENSOR API PARAM TABLE
#                                   #
# ================================= #
SELECT_SENS_API_PARAM_OF = "SELECT a.sensor_id, a.ch_key, a.ch_id, a.ch_name, a.last_acquisition " \
                           "FROM level0_raw.sensor_api_param AS a INNER JOIN level0_raw.sensor AS s " \
                           "ON s.id = a.sensor_id WHERE s.sensor_type ILIKE '%{type}%';"

SELECT_LAST_ACQUISITION_OF = "SELECT last_acquisition FROM level0_raw.sensor_api_param " \
                             "WHERE sensor_id = {sid} AND ch_name = '{ch}';"

UPDATE_LAST_CH_TIMEST      = "UPDATE level0_raw.sensor_api_param SET last_acquisition = '{time}' " \
                             "WHERE sensor_id = {sid} AND ch_name = '{ch}';"

INSERT_SENSOR_API_PARAM = "INSERT INTO level0_raw.sensor_api_param " \
                          "(sensor_id, ch_key, ch_id, ch_name, last_acquisition) VALUES {val};"

# ================================= #
#                                   #
# MOBILE MEASUREMENT TABLE
#                                   #
# ================================= #
SELECT_MAX_MOBILE_PACK_ID = "SELECT MAX(packet_id) FROM level0_raw.mobile_measurement;"

INSERT_MOBILE_MEASURES    = "INSERT INTO level0_raw.mobile_measurement " \
                            "(packet_id, param_id, param_value, timestamp, geom) VALUES {val};"

# ================================= #
#                                   #
# STATION MEASUREMENT TABLE
#                                   #
# ================================= #
SELECT_MAX_STATION_PACK_ID = "SELECT MAX(packet_id) FROM level0_raw.station_measurement;"

INSERT_STATION_MEASURES    = "INSERT INTO level0_raw.station_measurement " \
                             "(packet_id, sensor_id, param_id, param_value, timestamp) VALUES {val};"

# ================================= #
#                                   #
# SERVICE TABLE
#                                   #
# ================================= #
SELECT_SERVICE_ID_FROM = "SELECT id FROM level0_raw.service WHERE service_name ILIKE '%{sn}%';"

# ================================= #
#                                   #
# SERVICE API PARAM TABLE
#                                   #
# ================================= #
SELECT_SERVICE_API_PARAM_OF = "SELECT p.api_key, p.n_requests FROM level0_raw.service_api_param AS p " \
                              "INNER JOIN level0_raw.service AS s " \
                              "ON s.id = p.service_id " \
                              "WHERE s.service_name ILIKE '%{sn}%';"

# ================================= #
#                                   #
# GEOGRAPHICAL AREA TABLE
#                                   #
# ================================= #
SELECT_POSCODES_OF = "SELECT postal_code FROM level0_raw.geographical_area " \
                     "WHERE country_code = '{code}';"

SELECT_GEOLOCATION_OF = "SELECT id, ST_X(geom), ST_Y(geom) FROM level0_raw.geographical_area " \
                        "WHERE country_code = '{country}' AND place_name = '{place}';"

INSERT_PLACES      = "INSERT INTO level0_raw.geographical_area " \
                     "(service_id, postal_code, country_code, place_name, province, state, geom) VALUES {val};"

# ================================= #
#                                   #
# WEATHER CONDITION TABLE
#                                   #
# ================================= #
SELECT_WEATHER_COND = "SELECT id, code, icon FROM level0_raw.weather_condition;"

# ================================= #
#                                   #
# CURRENT WEATHER
#                                   #
# ================================= #
INSERT_CURRENT_WEATHER_DATA = "INSERT INTO level0_raw.current_weather " \
                              "(service_id, geoarea_id, weather_id, temperature, pressure, " \
                              "humidity, wind_speed, wind_direction, rain, snow, timestamp) VALUES {val};"

# ================================= #
#                                   #
# HOURLY FORECAST TABLE
#                                   #
# ================================= #
INSERT_HOURLY_FORECAST_DATA = "INSERT INTO level0_raw.hourly_forecast " \
                              "(service_id, geoarea_id, weather_id, temperature, pressure, " \
                              "humidity, wind_speed, wind_direction, rain, snow, timestamp) VALUES {val};"

DELETE_ALL_HOURLY_FORECAST = "DELETE FROM level0_raw.hourly_forecast;"

# ================================= #
#                                   #
# DAILY FORECAST TABLE
#                                   #
# ================================= #
INSERT_DAILY_FORECAST_DATA = "INSERT INTO level0_raw.daily_forecast " \
                             "(service_id, geoarea_id, weather_id, temperature, min_temp, max_temp, " \
                             "pressure, humidity, wind_speed, wind_direction, rain, snow, timestamp) VALUES {val};"

DELETE_ALL_DAILY_FORECAST = "DELETE FROM level0_raw.daily_forecast;"
