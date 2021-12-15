######################################################
#
# Author: Davide Colombo
# Date: 15/12/21 11:57
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Dict, Any


# class URLFormatter(object):
#
#     def __init__(self, url_template: str):
#         self.url_template = url_template
#
#     def format_url(self) -> str:
#         return self.url_template
#
#
# class AtmotubeURLFormatter(URLFormatter):
#
#     def with_date(self, external_options: Dict[str, Any]):
#         try:
#             date = external_options['date']
#             self.url_template += f"&date={date}"
#         except KeyError:
#             # TODO log warning
#             return
#
#
# class ThingspeakFormatter(URLFormatter):
#
#     def with_start_end(self, external_options: Dict[str, Any]):
#         try:
#             start = external_options['start'].replace(" ", "%20")
#             end = external_options['end'].replace(" ", "%20")
#             self.url_template += f"&start={start}&end={end}"
#         except KeyError:
#             # TODO log warning
#             return
