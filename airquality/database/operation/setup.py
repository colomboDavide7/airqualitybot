######################################################
#
# Author: Davide Colombo
# Date: 16/11/21 15:44
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.database.operation.insert as ins
import airquality.database.util.record.record as rec
import airquality.database.util.record.time as t
import airquality.database.util.record.location as loc
import airquality.database.util.datatype.timestamp as ts
import airquality.database.util.postgis.geom as geom


def setup_insert_wrapper(bot_name: str, sensor_type: str, insert_wrapper: ins.InsertWrapper) -> ins.InsertWrapper:

    # Get Timestamp class
    timest_class = ts.get_timest_class(sensor_type)
    # Build TimeRecord by injecting the Timestamp class
    time_rec = t.TimeRecord(timestamp_class=timest_class)

    # Get GeometryBuilder
    geom_builder = geom.PointBuilder()
    # Build LocationRecord by injecting the GeometryBuilder class
    location_rec = loc.LocationRecord(postgis_builder=geom_builder)

    # Setup for 'init' and 'update' bots
    if bot_name in ('init', 'update'):
        current_timestamp_time_record = t.CurrentTimestampTimeRecord()
        sensor_location_record_builder = rec.SensorLocationRecord(location_rec=location_rec, time_rec=current_timestamp_time_record)
        api_param_record_builder = rec.APIParamRecord()
        sensor_record_builder = rec.SensorRecord()
        sensor_info_record_builder = rec.SensorInfoRecord(time_rec=time_rec)

        # Inject InsertWrapper dependencies
        insert_wrapper.set_sensor_record_builder(sensor_record_builder)
        insert_wrapper.set_api_param_record_builder(api_param_record_builder)
        insert_wrapper.set_sensor_info_record_builder(sensor_info_record_builder)
        insert_wrapper.set_sensor_location_record_builder(sensor_location_record_builder)

    elif bot_name == 'fetch':
        if sensor_type == 'atmotube':
            mobile_record_builder = rec.MobileMeasureRecord(time_rec=time_rec, location_rec=location_rec)
            insert_wrapper.set_mobile_record_builder(mobile_record_builder)
        elif sensor_type == 'thingspeak':
            station_record_builder = rec.StationMeasureRecord(time_rec=time_rec)
            insert_wrapper.set_station_record_builder(station_record_builder)

    return insert_wrapper
