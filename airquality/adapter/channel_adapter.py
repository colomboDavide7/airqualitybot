######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 07/11/21 14:46
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List, Dict, Any
from airquality.constants.shared_constants import EXCEPTION_HEADER


class ChannelAdapter:

    def __init__(self, api_param: Dict[str, Any]):
        self.api_param = api_param

    def adapt(self) -> List[Dict[str, Any]]:
        reshaped_packets = []
        try:
            reshaped_packets.append(
                {'id': self.api_param['primary_id_a'],
                 'key': self.api_param['primary_key_a'],
                 'ts': self.api_param['primary_timestamp_a'],
                 'ts_name': 'primary_timestamp_a'}
            )
            reshaped_packets.append(
                {'id': self.api_param['primary_id_b'],
                 'key': self.api_param['primary_key_b'],
                 'ts': self.api_param['primary_timestamp_b'],
                 'ts_name': 'primary_timestamp_b'}
            )
            reshaped_packets.append(
                {'id': self.api_param['secondary_id_a'],
                 'key': self.api_param['secondary_key_a'],
                 'ts': self.api_param['secondary_timestamp_a'],
                 'ts_name': 'secondary_timestamp_a'}
            )
            reshaped_packets.append(
                {'id': self.api_param['secondary_id_b'],
                 'key': self.api_param['secondary_key_b'],
                 'ts': self.api_param['secondary_timestamp_b'],
                 'ts_name': 'secondary_timestamp_b'}
            )
        except KeyError as ke:
            raise SystemExit(f"{EXCEPTION_HEADER} {ChannelAdapter.__name__} missing key='{ke!s}'.")
        return reshaped_packets
