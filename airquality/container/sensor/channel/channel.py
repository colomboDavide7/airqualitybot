######################################################
#
# Author: Davide Colombo
# Date: 22/11/21 16:46
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.container.sensor.channel.param.api_param as api_c
import airquality.container.sensor.channel.channel_info as info_c


class ChannelContainer:

    def __init__(self, api_param_container: api_c.APIParamContainer, channel_info_container: info_c.ChannelInfoContainer):
        self.api_param_container = api_param_container
        self.channel_info_container = channel_info_container
