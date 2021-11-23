######################################################
#
# Author: Davide Colombo
# Date: 22/11/21 16:36
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.container.sensor.channel.param.param_name_val as par_c


class APIParamContainer:

    def __init__(self, ident: par_c.ParamNameValueContainer, key: par_c.ParamNameValueContainer):
        self.ident = ident
        self.key = key
