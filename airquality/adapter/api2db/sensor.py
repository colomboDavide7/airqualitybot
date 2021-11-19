######################################################
#
# Author: Davide Colombo
# Date: 12/11/21 17:28
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Dict, Any, List
import airquality.adapter.config as adapt_const
import airquality.database.util.postgis.config as geom_conf
import airquality.database.util.datatype.config as time_conf
import airquality.database.util.postgis.geom as geom
import airquality.database.util.datatype.timestamp as ts
import airquality.logger.loggable as log
import airquality.logger.util.decorator as log_decorator


def get_sensor_adapter(sensor_type: str, postgis_class=geom.PointBuilder, timestamp_class=ts.UnixTimestamp, log_filename="app"):
    if sensor_type == 'purpleair':
        return PurpleairSensorAdapter(postgis_class=postgis_class, timestamp_class=timestamp_class, log_filename=log_filename)
    else:
        raise SystemExit(f"'{get_sensor_adapter.__name__}():' bad type '{sensor_type}'")


################################ SENSOR ADAPTER CLASS ################################
class SensorAdapter(log.Loggable):

    def __init__(self, postgis_class=geom.GeometryBuilder, timestamp_class=ts.Timestamp, log_filename="app"):
        super(SensorAdapter, self).__init__(log_filename=log_filename)
        self.postgis_class = postgis_class
        self.timestamp_class = timestamp_class

    def _get_timestamp(self, timestamp: str) -> Dict[str, Any]:
        return {adapt_const.CLS: self.timestamp_class,
                adapt_const.KW: {time_conf.TIMEST_INIT_TIMESTAMP: timestamp}}

    @abc.abstractmethod
    def reshape(self, sensor_data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abc.abstractmethod
    def _get_sensor_name(self, data: Dict[str, Any]) -> str:
        pass

    @abc.abstractmethod
    def _get_sensor_info(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass

    @abc.abstractmethod
    def _get_api_param(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass

    @abc.abstractmethod
    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        pass


################################ PURPLEAIR SENSOR ADAPTER ################################
class PurpleairSensorAdapter(SensorAdapter):

    SENSOR_TYPE = 'PurpleAir/ThingSpeak'

    def __init__(self, postgis_class=geom.PointBuilder, timestamp_class=ts.UnixTimestamp, log_filename="app"):
        super(PurpleairSensorAdapter, self).__init__(postgis_class=postgis_class,
                                                     timestamp_class=timestamp_class,
                                                     log_filename=log_filename)

    @log_decorator.log_decorator()
    def reshape(self, data: Dict[str, Any]) -> Dict[str, Any]:
        self._exit_on_bad_sensor_data(sensor_data=data)
        uniformed_data = {adapt_const.SENS_NAME: self._get_sensor_name(data=data),
                          adapt_const.SENS_INFO: self._get_sensor_info(data=data),
                          adapt_const.SENS_GEOM: self._get_location(data=data),
                          adapt_const.SENS_PARAM: self._get_api_param(data=data),
                          adapt_const.TIMEST: {adapt_const.CLS: ts.CurrentTimestamp, adapt_const.KW: {}},
                          adapt_const.SENS_TYPE: PurpleairSensorAdapter.SENSOR_TYPE}
        return uniformed_data

    def _get_sensor_name(self, data: Dict[str, Any]) -> str:
        return f"{data['name']} ({data['sensor_index']})".replace("'", "")

    def _get_sensor_info(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [{adapt_const.SENS_CH: ch_n,
                 adapt_const.TIMEST: self._get_timestamp(timestamp=data['date_created'])} for ch_n in adapt_const.CHANNEL_NAMES]

    def _get_api_param(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [{adapt_const.PAR_NAME: n, adapt_const.PAR_VAL: data[n]} for n in adapt_const.API_PARAM]

    def _get_location(self, data: Dict[str, Any]) -> Dict[str, Any]:
        g = {adapt_const.CLS: geom.NullGeometry, adapt_const.KW: {}}
        if 'latitude' in data and 'longitude' in data:
            g = {adapt_const.CLS: self.postgis_class,
                 adapt_const.KW: {geom_conf.POINT_INIT_LAT_NAME: data['latitude'],
                                  geom_conf.POINT_INIT_LNG_NAME: data['longitude']}}
        return g

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        if 'name' not in sensor_data or 'sensor_index' not in sensor_data:
            raise SystemExit(f"{PurpleairSensorAdapter.__name__}: bad sensor data => missing fields 'name', 'sensor_index'")
        if 'latitude' not in sensor_data or 'longitude' not in sensor_data:
            raise SystemExit(f"{PurpleairSensorAdapter.__name__}: bad sensor data => missing fields 'latitude', 'longitude'")
        if 'date_created' not in sensor_data:
            raise SystemExit(f"{PurpleairSensorAdapter.__name__}: bad sensor data => missing field='date_created'")
        for n in adapt_const.API_PARAM:
            if n not in sensor_data:
                raise SystemExit(f"{PurpleairSensorAdapter.__name__}: bad sensor data => missing api param key='{n}'")
