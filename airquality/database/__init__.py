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
SELECT_SENS_API_PARAM_OF = "SELECT a.sensor_id, a.ch_key, a.ch_id, a.ch_name, a.last_acquisition FROM level0_raw.sensor_api_param AS a INNER JOIN level0_raw.sensor AS s ON s.id = a.sensor_id WHERE s.sensor_type ILIKE '%{type}%';"
SELECT_LAST_ACQUISITION_OF = "SELECT last_acquisition FROM level0_raw.sensor_api_param WHERE sensor_id = {sid} AND ch_name = '{ch}';"
SELECT_OPENWEATHERMAP_KEY = "SELECT key_value, done_req_min, max_req_min FROM level0_raw.openweathermap_key;"
SELECT_POSCODES_OF = "SELECT postal_code FROM level0_raw.geographical_area WHERE country_code = '{code}';"
SELECT_GEOLOCATION_OF = "SELECT id, ST_X(geom), ST_Y(geom) FROM level0_raw.geographical_area WHERE country_code = '{country}' AND place_name = '{place}';"
SELECT_FIXED_SENSOR_UNIQUE_INFO = "SELECT s.id, s.sensor_name, ST_X(l.geom), ST_Y(l.geom) FROM level0_raw.sensor AS s INNER JOIN level0_raw.sensor_at_location AS l ON s.id = l.sensor_id WHERE l.sensor_id = {sid} AND l.valid_to IS NULL;"
SELECT_MOBILE_SENSOR_UNIQUE_INFO = "SELECT id, sensor_name FROM level0_raw.sensor WHERE id = {sid};"
SELECT_PURPLEAIR_LOCATION = "SELECT ST_X(geom), ST_Y(geom) FROM level0_raw.sensor_at_location AS l INNER JOIN level0_raw.sensor AS s ON s.id = l.sensor_id WHERE s.sensor_type ILIKE '%purpleair%' AND sensor_name ILIKE '%{idx}%' ORDER BY l.valid_from DESC;"
