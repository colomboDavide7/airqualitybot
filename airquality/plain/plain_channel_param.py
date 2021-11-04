######################################################
#
# Owner: Davide Colombo
# User: davidecolombo
# Date: 04/11/21 08:48
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import builtins


class PlainChannelParamThingspeak(builtins.object):

    def __init__(self, channel_id: str, channel_key: str, channel_ts: str, ts_name: str):
        self.channel_id = channel_id
        self.channel_key = channel_key
        self.channel_ts = channel_ts
        self.ts_name = ts_name
