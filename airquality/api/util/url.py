#################################################
#
# Author: Davide Colombo
# @Date: mer, 20-10-2021, 09:52
# @Description: this script defines a simple factory class for building valid URL querystring based on sensor type.
#
#################################################
import abc
from typing import Dict, Any
import airquality.logger.loggable as log


def get_url_builder(sensor_type: str, address: str, url_param: Dict[str, Any]):

    if sensor_type == 'purpleair':
        return PurpleairURL(address=address, url_param=url_param)
    elif sensor_type == 'atmotube':
        return AtmotubeURL(address=address, url_param=url_param)
    elif sensor_type == 'thingspeak':
        return ThingspeakURL(address=address, url_param=url_param)
    else:
        raise SystemExit(f"'{get_url_builder.__name__}():' bad type '{sensor_type}'")


################################ URL BUILDER ################################
class URLBuilder(log.Loggable):

    def __init__(self, address: str, url_param: Dict[str, Any]):
        super(URLBuilder, self).__init__()
        self.address = address
        self.url_param = url_param

    @abc.abstractmethod
    def url(self) -> str:
        pass

    @abc.abstractmethod
    def _exit_on_bad_url_parameters(self):
        pass

    def _get_querystring(self):
        return '&'.join(f"{n}={v}" for n, v in self.url_param.items())


################################ PURPLEAIR URL BUILDER ################################
class PurpleairURL(URLBuilder):

    def __init__(self, address: str, url_param: Dict[str, Any]):
        super(PurpleairURL, self).__init__(address=address, url_param=url_param)

    def url(self) -> str:

        self.log_info(f"{PurpleairURL.__name__}: try to build URL...")
        self._exit_on_bad_url_parameters()
        url = f"{self.address}?{self._get_fields_string()}&{self._get_querystring()}"
        self.log_info(f"{PurpleairURL.__name__}: done")
        return url

    def _get_fields_string(self) -> str:
        return "fields=" + ','.join(f"{f}" for f in self.url_param.pop('fields'))

    def _exit_on_bad_url_parameters(self):
        if 'api_key' not in self.url_param:
            raise SystemExit(f"{PurpleairURL.__name__}: bad url param => missing key='api_key'")
        elif 'fields' not in self.url_param:
            raise SystemExit(f"{PurpleairURL.__name__}: bad url param => missing key='fields'")
        elif not self.url_param['fields']:
            raise SystemExit(f"{PurpleairURL.__name__}: bad url param => empty fields.")


################################ ATMOTUBE URL BUILDER ################################
class AtmotubeURL(URLBuilder):

    def __init__(self, address: str, url_param: Dict[str, Any]):
        super(AtmotubeURL, self).__init__(address=address, url_param=url_param)

    def url(self) -> str:

        self.log_info(f"{AtmotubeURL.__name__}: try to build URL...")
        self._exit_on_bad_url_parameters()
        url = f"{self.address}?{self._get_querystring()}"
        self.log_info(f"{AtmotubeURL.__name__}: done")
        return url

    def _exit_on_bad_url_parameters(self):
        if 'api_key' not in self.url_param:
            raise SystemExit(f"{AtmotubeURL.__name__}: bad url param => missing key='api_key'")
        elif 'mac' not in self.url_param:
            raise SystemExit(f"{AtmotubeURL.__name__}: bad url param => missing key='mac'")


################################ THINGSPEAK URL BUILDER ################################
class ThingspeakURL(URLBuilder):

    def __init__(self, address: str, url_param: Dict[str, Any]):
        super(ThingspeakURL, self).__init__(address=address, url_param=url_param)

        if 'format' not in self.url_param:
            raise SystemExit(f"{ThingspeakURL.__name__}: bad 'api.json' file structure => missing key='format'")
        self.response_fmt = self.url_param.pop('format')

    def url(self) -> str:

        self.log_info(f"{ThingspeakURL.__name__}: try to build URL...")
        self._exit_on_bad_url_parameters()
        url = f"{self.address}/{self.url_param['channel_id']}/feeds.{self.response_fmt}?{self._get_querystring()}"
        self.log_info(f"{ThingspeakURL.__name__}: done")
        return url.replace(' ', '%20')

    def _get_querystring(self):
        return '&'.join(f"{n}={v}" for n, v in self.url_param.items() if n != 'channel_id')

    def _exit_on_bad_url_parameters(self):
        if 'api_key' not in self.url_param:
            raise SystemExit(f"{ThingspeakURL.__name__}: bad url param => missing key='api_key'")
        elif 'channel_id' not in self.url_param:
            raise SystemExit(f"{ThingspeakURL.__name__}: bad url param => missing key='channel_id'")
