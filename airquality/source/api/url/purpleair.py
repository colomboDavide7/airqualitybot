######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:33
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.source.api.url.abc as base


# ------------------------------- PurpleairURLBuilder ------------------------------- #
class PurpleairURLBuilder(base.URLBuilderABC):

    def __init__(self, url_template: str):
        super(PurpleairURLBuilder, self).__init__(url_template=url_template)

    ################################ build() ################################
    def build(self) -> str:
        return self.url_template
