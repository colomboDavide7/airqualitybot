######################################################
#
# Author: Davide Colombo
# Date: 23/11/21 16:32
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any
import airquality.api.url.timeurl as tmurl


class AtmotubeURLBuilder(tmurl.dyn.DynamicURLBuilder):

    def __init__(self, address: str, options: Dict[str, Any]):
        super(AtmotubeURLBuilder, self).__init__(address=address, options=options)

    def build(self) -> str:
        return f"{self.address}?api_key={self.api_key}&mac={self.identifier}&{self._get_options_querystring()}"


class AtmotubeTimeURLBuilder(tmurl.TimeURLBuilder):

    def __init__(self, target: AtmotubeURLBuilder, step_size_in_days: int = 1):
        super(AtmotubeTimeURLBuilder, self).__init__(target=target, step_size_in_days=step_size_in_days)
        self.date = None

    def build(self) -> str:
        self.get_next_date()
        basic_url = self.target.build()
        basic_url += f"&date={self.date}"
        return basic_url

    def get_next_date(self):
        current_date = self.start_ts
        if current_date.is_after(self.stop_ts) or current_date.is_same_day(self.stop_ts):
            self.ended = True
            current_date = self.stop_ts
        self.start_ts = self.start_ts.add_days(self.step_size_in_days)
        self.date = current_date.ts.split(' ')[0]
