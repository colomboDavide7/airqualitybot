######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 14/11/21 11:37
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import abc


def get_file_adapter_class(sensor_type: str):

    if sensor_type == 'purpleair':
        return PurpleairEnvAdapter
    else:
        raise SystemExit(f"'{get_file_adapter_class.__name__}()': "
                         f"bad type => {EnvAdapter.__name__} undefined for type='{sensor_type}'")


class EnvAdapter(abc.ABC):

    @abc.abstractmethod
    def adapt(self):
        pass


class PurpleairEnvAdapter(EnvAdapter):

    def __init__(self):
        if not os.environ.get('PURPLEAIR_KEY1'):
            raise SystemExit(f"{PurpleairEnvAdapter.__name__}: bad '.env' file structure => missing param='PURPLEAIR_KEY1'")
        self.key1 = os.environ['PURPLEAIR_KEY1']

    def adapt(self):
        return {'api_key': self.key1}


# class AtmotubeEnvAdapter(EnvAdapter):
#
#     def adapt(self):
#         env_param = []
#         for key in os.environ.keys():
#             if key.startswith('ATMOTUBE'):
#                 sensor_str = os.environ[key]
#                 try:
#                     api_key, mac, name = sensor_str.split(', ')
#                 except ValueError as ve:
#                     raise SystemExit(f"'{AtmotubeEnvAdapter.__name__}': bad '.env' file structure => sensor string is "
#                                      f"missing one of three values at key='{key}'")
#                 env_param.append({'api_key': api_key, 'mac': mac, 'name': name})
#         return env_param
