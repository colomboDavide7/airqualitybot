#################################################
#
# @Author: davidecolombo
# @Date: mer, 20-10-2021, 09:52
# @Description: this script defines a simple factory class for building valid URL querystring based on sensor type.
#
#################################################
import abc
from typing import Dict, Any

EQ = '='
AND = '&'
QU = '?'


def get_url_class(sensor_type: str):

    if sensor_type == 'purpleair':
        return PurpleairURL
    elif sensor_type == 'atmotube':
        return AtmotubeURL
    elif sensor_type == 'thingspeak':
        return ThingspeakURL


class URLBuilder(abc.ABC):

    def __init__(self, address: str, url_param: Dict[str, Any]):
        self.address = address
        self.url_param = url_param

    @abc.abstractmethod
    def url(self) -> str:
        pass

    def update_param(self, sensor_param: Dict[str, Any]):
        tmp = self.url_param.copy()
        tmp.update(sensor_param)
        self.url_param = tmp


class PurpleairURL(URLBuilder):

    def __init__(self, address: str, url_param: Dict[str, Any]):
        super(PurpleairURL, self).__init__(address=address, url_param=url_param)

    def url(self) -> str:
        if 'api_key' not in self.url_param:
            raise SystemExit(f"{PurpleairURL.__name__}: bad 'api.json' file structure => missing key='api_key'")
        elif 'fields' not in self.url_param:
            raise SystemExit(f"{PurpleairURL.__name__}: bad 'api.json' file structure => missing key='fields'")
        elif not self.url_param['fields']:
            raise SystemExit(f"{PurpleairURL.__name__}: bad 'api.json' file structure => empty fields.")

        url = self.address + QU
        for param_name, param_value in self.url_param.items():
            if param_name == 'fields':
                url += 'fields='
                for field in param_value:
                    url += f"{field},"
                url = url.strip(',') + AND
            else:
                url += f"{param_name}={param_value}&"
        return url.strip(AND)


class AtmotubeURL(URLBuilder):

    def __init__(self, address: str, url_param: Dict[str, Any]):
        super(AtmotubeURL, self).__init__(address=address, url_param=url_param)

    def url(self) -> str:
        if 'api_key' not in self.url_param:
            raise SystemExit(f"{AtmotubeURL.__name__}: bad 'api.json' file structure => missing key='api_key'")
        elif 'mac' not in self.url_param:
            raise SystemExit(f"{AtmotubeURL.__name__}: bad 'api.json' file structure => missing key='mac'")

        url = self.address + QU
        for param_name, param_value in self.url_param.items():
            url += f"{param_name}={param_value}&"
        return url.strip(AND)


class ThingspeakURL(URLBuilder):

    def __init__(self, address: str, url_param: Dict[str, Any]):
        super(ThingspeakURL, self).__init__(address=address, url_param=url_param)
        if 'format' not in self.url_param:
            raise SystemExit(f"{ThingspeakURL.__name__}: bad 'api.json' file structure => missing key='format'")
        self.address_fmt = 'feeds.' + self.url_param.pop('format')

    def url(self) -> str:
        if 'api_key' not in self.url_param:
            raise SystemExit(f"{ThingspeakURL.__name__}: bad 'api.json' file structure => missing key='api_key'")
        elif 'channel_id' not in self.url_param:
            raise SystemExit(f"{ThingspeakURL.__name__}: bad 'api.json' file structure => missing key='channel_id'")

        url = self.address + '/' + self.url_param.pop('channel_id') + '/'
        url += self.address_fmt + QU
        for param_name, param_value in self.url_param.items():
            url += f"{param_name}={param_value}&"
        return url.strip(AND)
