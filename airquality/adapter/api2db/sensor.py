######################################################
#
# Author: Davide Colombo
# Date: 12/11/21 17:28
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Dict, Any, List
import airquality.adapter.config as c
import airquality.database.util.postgis.geom as geom
import airquality.database.util.datatype.timestamp as ts


def get_sensor_adapter(sensor_type: str, postgis_class=geom.PointBuilder, timestamp_class=ts.UnixTimestamp):
    if sensor_type == 'purpleair':
        return PurpleairSensorAdapter(postgis_class=postgis_class, timestamp_class=timestamp_class)
    else:
        raise SystemExit(f"'{get_sensor_adapter.__name__}():' bad type '{sensor_type}'")


################################ SENSOR ADAPTER CLASS ################################
class SensorAdapter(abc.ABC):

    def __init__(self, postgis_class=geom.GeometryBuilder, timestamp_class=ts.Timestamp):
        self.postgis_class = postgis_class
        self.timestamp_class = timestamp_class

    def _get_timestamp(self, timestamp: str) -> Dict[str, Any]:
        return {c.CLS: self.timestamp_class, c.KW: {'timestamp': timestamp}}

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
    API_PARAM = ['primary_id_a', 'primary_id_b', 'primary_key_a', 'primary_key_b',
                 'secondary_id_a', 'secondary_id_b', 'secondary_key_a', 'secondary_key_b']

    def __init__(self, postgis_class=geom.PointBuilder, timestamp_class=ts.UnixTimestamp):
        super(PurpleairSensorAdapter, self).__init__(postgis_class=postgis_class, timestamp_class=timestamp_class)

    def reshape(self, data: Dict[str, Any]) -> Dict[str, Any]:
        self._exit_on_bad_sensor_data(sensor_data=data)
        uniformed_data = {c.SENS_NAME: self._get_sensor_name(data=data),
                          c.
                          : self._get_sensor_info(data=data),
                          c.SENS_GEOM: self._add_location(data=data),
                          c.SENS_PARAM: self._get_api_param(data=data),
                          c.TIMEST: {c.CLS: ts.CurrentTimestamp, c.KW: {}},
                          c.SENS_TYPE: PurpleairSensorAdapter.SENSOR_TYPE}
        return uniformed_data

    def _get_sensor_name(self, data: Dict[str, Any]) -> str:
        return f"{data['name']} ({data['sensor_index']})".replace("'", "")

    def _get_sensor_info(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [{c.SENS_CH: ch_n, c.TIMEST: self._get_timestamp(timestamp=data['date_created'])} for ch_n in c.CHANNEL_NAMES]

    def _get_api_param(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [{c.PAR_NAME: n, c.PAR_VAL: data[n]} for n in PurpleairSensorAdapter.API_PARAM]

    def _add_location(self, data: Dict[str, Any]) -> Dict[str, Any]:
        g = {c.CLS: geom.NullGeometry, c.KW: {}}
        if 'latitude' in data and 'longitude' in data:
            g = {c.CLS: self.postgis_class, c.KW: {'lat': data['latitude'], 'lng': data['longitude']}}
        return g

    def _exit_on_bad_sensor_data(self, sensor_data: Dict[str, Any]):
        if 'name' not in sensor_data or 'sensor_index' not in sensor_data:
            raise SystemExit(f"{PurpleairSensorAdapter.__name__}: bad sensor data => missing fields 'name', 'sensor_index'")
        if 'latitude' not in sensor_data or 'longitude' not in sensor_data:
            raise SystemExit(f"{PurpleairSensorAdapter.__name__}: bad sensor data => missing fields 'latitude', 'longitude'")
        if 'date_created' not in sensor_data:
            raise SystemExit(f"{PurpleairSensorAdapter.__name__}: bad sensor data => missing field='date_created'")
        for n in PurpleairSensorAdapter.API_PARAM:
            if n not in sensor_data:
                raise SystemExit(f"{PurpleairSensorAdapter.__name__}: bad sensor data => missing api param key='{n}'")
