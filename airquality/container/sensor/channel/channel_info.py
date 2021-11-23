######################################################
#
# Author: Davide Colombo
# Date: 22/11/21 16:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.database.util.datatype.timestamp as ts


class ChannelInfoContainer:

    def __init__(self, name: str, last_acquisition: ts.Timestamp):
        self.name = name
        self.last_acquisition = last_acquisition
