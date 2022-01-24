# ======================================
# @author:  Davide Colombo
# @date:    2022-01-18, mar, 11:49
# ======================================

SELECT_MAX_SENS_ID = "SELECT MAX(id) FROM level0_raw.sensor;"
SELECT_MAX_MOBILE_PACK_ID = "SELECT MAX(packet_id) FROM level0_raw.mobile_measurement;"
SELECT_MAX_STATION_PACK_ID = "SELECT MAX(packet_id) FROM level0_raw.station_measurement;"

SELECT_WEATHER_COND = "SELECT id, code, icon FROM level0_raw.weather_condition;"
SELECT_MEASURE_PARAM = "SELECT id, param_code FROM level0_raw.measure_param WHERE param_owner ILIKE '%{owner}%';"
SELECT_SENSOR_NAMES = "SELECT sensor_name FROM level0_raw.sensor WHERE sensor_type ILIKE '%{type}%';"
SELECT_SERVICE_ID_FROM = "SELECT id FROM level0_raw.service WHERE service_name ILIKE '%{sn}%';"
SELECT_SENS_API_PARAM_OF = "SELECT a.sensor_id, a.ch_key, a.ch_id, a.ch_name, a.last_acquisition FROM level0_raw.sensor_api_param AS a INNER JOIN level0_raw.sensor AS s ON s.id = a.sensor_id WHERE s.sensor_type ILIKE '%{type}%';"
SELECT_LAST_ACQUISITION_OF = "SELECT last_acquisition FROM level0_raw.sensor_api_param WHERE sensor_id = {sid} AND ch_name = '{ch}';"
SELECT_SERVICE_API_PARAM_OF = "SELECT p.api_key, p.n_requests FROM level0_raw.service_api_param AS p INNER JOIN level0_raw.service AS s ON s.id = p.service_id WHERE s.service_name ILIKE '%{sn}%';"
SELECT_POSCODES_OF = "SELECT postal_code FROM level0_raw.geographical_area WHERE country_code = '{code}';"
SELECT_GEOLOCATION_OF = "SELECT id, ST_X(geom), ST_Y(geom) FROM level0_raw.geographical_area WHERE country_code = '{country}' AND place_name = '{place}';"
SELECT_FIXED_SENSOR_UNIQUE_INFO = "SELECT s.id, s.sensor_name, ST_X(l.geom), ST_Y(l.geom) FROM level0_raw.sensor AS s INNER JOIN level0_raw.sensor_at_location AS l ON s.id = l.sensor_id WHERE l.sensor_id = {sid} AND l.valid_to IS NULL;"
SELECT_MOBILE_SENSOR_UNIQUE_INFO = "SELECT id, sensor_name FROM level0_raw.sensor WHERE id = {sid};"

# =========== INSERT QUERIES
INSERT_SENSORS = "INSERT INTO level0_raw.sensor VALUES {val};"
INSERT_SENSOR_LOCATION = "INSERT INTO level0_raw.sensor_at_location (sensor_id, valid_from, geom) VALUES {val};"
INSERT_SENSOR_API_PARAM = "INSERT INTO level0_raw.sensor_api_param (sensor_id, ch_key, ch_id, ch_name, last_acquisition) VALUES {val};"
INSERT_MOBILE_MEASURES = "INSERT INTO level0_raw.mobile_measurement (packet_id, param_id, param_value, timestamp, geom) VALUES {val};"
INSERT_STATION_MEASURES = "INSERT INTO level0_raw.station_measurement (packet_id, sensor_id, param_id, param_value, timestamp) VALUES {val};"
INSERT_PLACES = "INSERT INTO level0_raw.geographical_area (service_id, postal_code, country_code, place_name, province, state, geom) VALUES {val};"
INSERT_CURRENT_WEATHER_DATA = "INSERT INTO level0_raw.current_weather (service_id, geoarea_id, weather_id, temperature, pressure, humidity, wind_speed, wind_direction, rain, snow, timestamp) VALUES {val};"
INSERT_HOURLY_FORECAST_DATA = "INSERT INTO level0_raw.hourly_forecast (service_id, geoarea_id, weather_id, temperature, pressure, humidity, wind_speed, wind_direction, rain, snow, timestamp) VALUES {val};"
INSERT_DAILY_FORECAST_DATA = "INSERT INTO level0_raw.daily_forecast (service_id, geoarea_id, weather_id, temperature, min_temp, max_temp, pressure, humidity, wind_speed, wind_direction, rain, snow, timestamp) VALUES {val};"

# =========== UPDATE QUERIES
UPDATE_LAST_CH_TIMEST = "UPDATE level0_raw.sensor_api_param SET last_acquisition = '{time}' WHERE sensor_id = {sid} AND ch_name = '{ch}';"

# =========== DELETE QUERIES
DELETE_ALL_HOURLY_FORECAST = "DELETE FROM level0_raw.hourly_forecast;"
DELETE_ALL_DAILY_FORECAST = "DELETE FROM level0_raw.daily_forecast;"
