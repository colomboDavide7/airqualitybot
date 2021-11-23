######################################################
#
# Author: Davide Colombo
# Date: 22/11/21 16:48
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import List
import container.sensor.channel.channel as ch_c
import container.sensor.location.location as loc_c
import container.sensor.identity.identity as idt_c


class SensorContainer:

    def __init__(self, identity: idt_c.IdentityContainer, channels: List[ch_c.ChannelContainer], location: loc_c.LocationContainer):
        self.identity = identity
        self.channels = channels
        self.location = location
