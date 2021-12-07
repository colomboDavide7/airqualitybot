######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:33
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.api.url.baseurl as base


class PurpleairURLBuilder(base.BaseURLBuilder):

    def __init__(self, url_template: str):
        super(PurpleairURLBuilder, self).__init__(url_template=url_template)

    def build(self) -> str:
        return self.url_template
