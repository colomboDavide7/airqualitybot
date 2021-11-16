#################################################
#
# Author: Davide Colombo
# @Date: mer, 20-10-2021, 09:52
# @Description: this script defines a simple factory class for building valid URL querystring based on sensor type.
#
#################################################
import abc
from typing import Dict, Any

EQ = '='
AND = '&'
QU = '?'


def get_url_builder(sensor_type: str, address: str, url_param: Dict[str, Any]):

    if sensor_type == 'purpleair':
        return PurpleairURL(address=address, url_param=url_param)
    elif sensor_type == 'atmotube':
        return AtmotubeURL(address=address, url_param=url_param)
    elif sensor_type == 'thingspeak':
        return ThingspeakURL(address=address, url_param=url_param)


################################ URL BUILDER ################################
class URLBuilder(abc.ABC):

    def __init__(self, address: str, url_param: Dict[str, Any]):
        self.address = address
        self.url_param = url_param

    @abc.abstractmethod
    def url(self) -> str:
        pass


################################ PURPLEAIR URL BUILDER ################################
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


################################ ATMOTUBE URL BUILDER ################################
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


################################ THINGSPEAK URL BUILDER ################################
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

        channel_id = self.url_param.pop('channel_id')
        url = self.address + '/' + channel_id + '/'
        url += self.address_fmt + QU
        for param_name, param_value in self.url_param.items():
            url += f"{param_name}={param_value}&"
        self.url_param['channel_id'] = channel_id
        return url.strip(AND)
