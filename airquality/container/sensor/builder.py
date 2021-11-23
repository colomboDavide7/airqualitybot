######################################################
#
# Author: Davide Colombo
# Date: 12/11/21 17:28
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import abc
from typing import Dict, Any
# Logger import
import airquality.logger.loggable as log
import airquality.logger.util.decorator as log_decorator
# Database import
import airquality.database.util.postgis.geom as geom
import airquality.database.util.postgis.config as postgis_conf
import airquality.database.util.datatype.timestamp as ts
# Container import
import container.sensor.sensor as sensor_c
import container.sensor.channel.channel as ch_c
import container.sensor.channel.channel_info as ch_info_c
import container.sensor.channel.param.api_param as api_param_c
import container.sensor.channel.param.param_name_val as name_val_c
import container.sensor.location.location as loc_c
import container.sensor.identity.identity as sens_ident_c


################################ SENSOR CONTAINER BUILDER ################################
class SensorContainerBuilder(log.Loggable):

    def __init__(self, postgis_class=geom.PostgisGeometry, timestamp_class=ts.Timestamp, log_filename="log"):
        super(SensorContainerBuilder, self).__init__(log_filename=log_filename)
        self.postgis_class = postgis_class
        self.timestamp_class = timestamp_class

    @abc.abstractmethod
    def build(self, data: Dict[str, Any], sensor_id: int) -> sensor_c.SensorContainer:
        pass

    @abc.abstractmethod
    def _build_channel(self, channel_name: str, ident_name: str, key_name: str, data: Dict[str, Any]) -> ch_c.ChannelContainer:
        pass

    @abc.abstractmethod
    def _build_location(self, data: Dict[str, Any]) -> loc_c.LocationContainer:
        pass


################################ PURPLEAIR SENSOR CONTAINER BUILDER ################################
class PurpleairSensorContainerBuilder(SensorContainerBuilder):

    def __init__(self, postgis_class=geom.PostgisPoint, timestamp_class=ts.UnixTimestamp, log_filename="log"):
        super(PurpleairSensorContainerBuilder, self).__init__(postgis_class=postgis_class, timestamp_class=timestamp_class,
                                                              log_filename=log_filename)
        self.name = "name"
        self.type = "PurpleAir/ThingSpeak"
        self.sensor_index = "sensor_index"
        self.primary_id_a = "primary_id_a"
        self.primary_key_a = "primary_key_a"
        self.primary_id_b = "primary_id_b"
        self.primary_key_b = "primary_key_b"
        self.secondary_id_a = "secondary_id_a"
        self.secondary_key_a = "secondary_key_a"
        self.secondary_id_b = "secondary_id_b"
        self.secondary_key_b = "secondary_key_b"
        self.latitude = "latitude"
        self.longitude = "longitude"
        self.date_created = "date_created"

    @log_decorator.log_decorator()
    def build(self, data: Dict[str, Any], sensor_id: int) -> sensor_c.SensorContainer:
        try:
            sensor_name = f"{data[self.name]} ({data[self.sensor_index]})".replace("'", "")
            identity = sens_ident_c.IdentityContainer(id_=sensor_id, name=sensor_name, type_=self.type)

            channels = [self._build_channel(channel_name='Primary data - channel A',
                                            ident_name=self.primary_id_a,
                                            key_name=self.primary_key_a,
                                            data=data),
                        self._build_channel(channel_name='Primary data - channel B',
                                            ident_name=self.primary_id_b,
                                            key_name=self.primary_key_b,
                                            data=data),
                        self._build_channel(channel_name='Secondary data - channel A',
                                            ident_name=self.secondary_id_a,
                                            key_name=self.secondary_key_a,
                                            data=data),
                        self._build_channel(channel_name='Secondary data - channel B',
                                            ident_name=self.secondary_id_b,
                                            key_name=self.secondary_key_b,
                                            data=data)]

            location = self._build_location(data=data)

        except KeyError as ke:
            raise SystemExit(f"{PurpleairSensorContainerBuilder.__name__}: bad sensor data => missing key={ke!s}")
        return sensor_c.SensorContainer(identity=identity, channels=channels, location=location)

    def _build_channel(self, channel_name: str, ident_name: str, key_name: str, data: Dict[str, Any]) -> ch_c.ChannelContainer:
        channel_ident_container = name_val_c.ParamNameValueContainer(name=ident_name, value=data[ident_name])
        channel_key_container = name_val_c.ParamNameValueContainer(name=key_name, value=data[key_name])
        channel_api_param = api_param_c.APIParamContainer(ident=channel_ident_container, key=channel_key_container)
        channel_last_acquisition = self.timestamp_class(timest=data[self.date_created])
        channel_info = ch_info_c.ChannelInfoContainer(name=channel_name, last_acquisition=channel_last_acquisition)
        return ch_c.ChannelContainer(api_param_container=channel_api_param, channel_info_container=channel_info)

    def _build_location(self, data: Dict[str, Any]) -> loc_c.LocationContainer:
        kwargs = {postgis_conf.POINT_INIT_LAT_NAME: data[self.latitude], postgis_conf.POINT_INIT_LNG_NAME: data[self.longitude]}
        postgis_geom = self.postgis_class(**kwargs)
        return loc_c.LocationContainer(valid_from=ts.CurrentTimestamp(), postgis_geom=postgis_geom)
