#################################################
#
# @Author: davidecolombo
# @Date: mer, 27-10-2021, 15:13
# @Description: this script defines the classes for reshaping data coming from database in order to make them compliant
#               with API needs.
#
#################################################
import builtins
from typing import List
from abc import ABC, abstractmethod
from airquality.plain.plain_api_param import PlainAPIParamThingspeak
from airquality.plain.plain_channel_param import PlainChannelParamThingspeak


class Database2APIReshaper(ABC):

    @abstractmethod
    def reshape_data(self, plain_api_param):
        """See subclass method implementation for arguments type."""
        pass


class Database2APIReshaperThingspeak(Database2APIReshaper):

    def reshape_data(self, plain_api_param: PlainAPIParamThingspeak) -> List[PlainChannelParamThingspeak]:
        channel_list = [PlainChannelParamThingspeak(channel_id=plain_api_param.primary_id_a,
                                                    channel_key=plain_api_param.primary_key_a,
                                                    channel_ts=plain_api_param.primary_timestamp_a,
                                                    ts_name='primary_timestamp_a'),
                        PlainChannelParamThingspeak(channel_id=plain_api_param.primary_id_b,
                                                    channel_key=plain_api_param.primary_key_b,
                                                    channel_ts=plain_api_param.primary_timestamp_b,
                                                    ts_name='primary_timestamp_b'),
                        PlainChannelParamThingspeak(channel_id=plain_api_param.secondary_id_a,
                                                    channel_key=plain_api_param.secondary_key_a,
                                                    channel_ts=plain_api_param.secondary_timestamp_a,
                                                    ts_name='secondary_timestamp_a'),
                        PlainChannelParamThingspeak(channel_id=plain_api_param.secondary_id_b,
                                                    channel_key=plain_api_param.secondary_key_b,
                                                    channel_ts=plain_api_param.secondary_timestamp_b,
                                                    ts_name='secondary_timestamp_b')]
        return channel_list


################################ FACTORY ################################
class Database2APIReshaperFactory(builtins.object):

    @classmethod
    def create_reshaper(cls, bot_personality: str) -> Database2APIReshaper:

        if bot_personality == "thingspeak":
            return Database2APIReshaperThingspeak()
        else:
            raise SystemExit(
                f"{Database2APIReshaperFactory.__name__}: cannot instantiate {Database2APIReshaper.__name__} "
                f"instance for personality='{bot_personality}'.")
