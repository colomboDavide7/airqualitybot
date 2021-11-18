######################################################
#
# Author: Davide Colombo
# Date: 12/11/21 17:20
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Dict, Any, List
import airquality.adapter.config as adapt_const
import airquality.database.util.postgis.config as geom_const
import airquality.database.operation.select.type as sel
import airquality.database.util.postgis.geom as postgis
import airquality.database.util.datatype.timestamp as ts


class MeasureAdapter(abc.ABC):

    def __init__(self, sel_type: sel.TypeSelectWrapper, geom_cls=postgis.GeometryBuilder, timest_cls=ts.Timestamp):
        self.measure_param_map = sel_type.get_measure_param()
        self.geom_cls = geom_cls
        self.timest_cls = timest_cls

    @abc.abstractmethod
    def reshape(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abc.abstractmethod
    def _get_measure_param_id_value(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        pass

    @abc.abstractmethod
    def _get_timestamp(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abc.abstractmethod
    def _exit_on_bad_sensor_data(self, data: Dict[str, Any]):
        pass


################################ INJECT ADAPTER DEPENDENCIES ################################
class AtmotubeMeasureAdapter(MeasureAdapter):

    ATMOTUBE_PARAM_NAMES = ['voc', 'pm1', 'pm25', 'pm10', 't', 'h', 'p']

    def __init__(self, sel_type: sel.TypeSelectWrapper, geom_cls=postgis.PointBuilder, timest_cls=ts.AtmotubeTimestamp):
        super(AtmotubeMeasureAdapter, self).__init__(sel_type=sel_type, geom_cls=geom_cls, timest_cls=timest_cls)
        self.record_id = sel_type.get_max_record_id()

    def reshape(self, data: Dict[str, Any]) -> Dict[str, Any]:
        self._exit_on_bad_sensor_data(data=data)
        uniformed_data = {adapt_const.REC_ID: self.record_id,
                          adapt_const.SENS_PARAM: self._get_measure_param_id_value(data=data),
                          adapt_const.SENS_GEOM: self._get_geometry(data=data),
                          adapt_const.TIMEST: self._get_timestamp(data=data)}
        self.record_id += 1
        return uniformed_data

    def _get_timestamp(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {adapt_const.CLS: self.timest_cls, adapt_const.KW: {'timestamp': data['time']}}

    def _get_measure_param_id_value(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [{adapt_const.PAR_ID: self.measure_param_map[n], adapt_const.PAR_VAL: data.get(n)} for n in AtmotubeMeasureAdapter.ATMOTUBE_PARAM_NAMES]

    def _get_geometry(self, data: Dict[str, Any]) -> Dict[str, Any]:
        geom = {adapt_const.CLS: postgis.NullGeometry, adapt_const.KW: {}}
        if data.get('coords') is not None:
            geom = {adapt_const.CLS: self.geom_cls,
                    adapt_const.KW: {geom_const.POINT_INIT_LAT_NAME: data['coords']['lat'],
                                     geom_const.POINT_INIT_LNG_NAME: data['coords']['lon']}}
        return geom

    def _exit_on_bad_sensor_data(self, data: Dict[str, Any]):
        if 'time' not in data:
            raise SystemExit(f"{AtmotubeMeasureAdapter.__name__}: bad sensor data => missing key='time'")


################################ INJECT ADAPTER DEPENDENCIES ################################
import airquality.api.config as extr_const


class ThingspeakMeasureAdapter(MeasureAdapter):

    def __init__(self, sel_type: sel.TypeSelectWrapper, timest_cls=ts.ThingspeakTimestamp):
        super(ThingspeakMeasureAdapter, self).__init__(sel_type=sel_type, timest_cls=timest_cls)
        self.record_id = sel_type.get_max_record_id()

    def reshape(self, data: Dict[str, Any]) -> Dict[str, Any]:
        self._exit_on_bad_sensor_data(data=data)
        uniformed_data = {adapt_const.REC_ID: self.record_id,
                          adapt_const.SENS_PARAM: self._get_measure_param_id_value(data=data),
                          adapt_const.TIMEST: self._get_timestamp(data=data)}
        self.record_id += 1
        return uniformed_data

    def _get_timestamp(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {adapt_const.CLS: self.timest_cls, adapt_const.KW: {'timestamp': data['created_at']}}

    def _get_measure_param_id_value(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [{adapt_const.PAR_ID: self.measure_param_map[f[extr_const.FIELD_NAME]], adapt_const.PAR_VAL: f[extr_const.FIELD_VALUE]}
                for f in data[extr_const.FIELDS]]

    def _exit_on_bad_sensor_data(self, data: Dict[str, Any]):
        if 'created_at' not in data:
            raise SystemExit(f"{ThingspeakMeasureAdapter.__name__}: bad sensor data => missing key='created_at'")
        if extr_const.FIELDS not in data:
            raise SystemExit(f"{ThingspeakMeasureAdapter.__name__}: bad sensor data => missing key='{extr_const.FIELDS}'")
        for f in data[extr_const.FIELDS]:
            if extr_const.FIELD_NAME not in f or extr_const.FIELD_VALUE not in f:
                raise SystemExit(f"{ThingspeakMeasureAdapter.__name__}: bad sensor data => '{extr_const.FIELDS}'"
                                 f" must contain '{extr_const.FIELD_NAME}' and '{extr_const.FIELD_VALUE}' keys")


################################ FUNCTION FOR GETTING MEASURE ADAPTER ################################
def get_measure_adapter(sensor_type: str, sel_type: sel.TypeSelectWrapper, geom_cls, timest_cls) -> MeasureAdapter:

    if sensor_type == 'atmotube':
        return AtmotubeMeasureAdapter(sel_type=sel_type, geom_cls=geom_cls,
                                      timest_cls=timest_cls)
    elif sensor_type == 'thingspeak':
        return ThingspeakMeasureAdapter(sel_type=sel_type, timest_cls=timest_cls)
    else:
        raise SystemExit(f"'{get_measure_adapter.__name__}():' bad type '{sensor_type}'")
