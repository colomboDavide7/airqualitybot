######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 17:49
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
from typing import Union
import airquality.command.basecmd as base
import airquality.logger.util.decorator as log_decorator
import airquality.api.fetchwrp as apiwrp
import airquality.database.op.ins.mbmeasins as ins
import airquality.database.op.sel.mobilesel as mbsel
import airquality.database.op.sel.stationsel as stsel
import database.dtype.timestamp as ts
import airquality.filter.tsfilt as flt
import airquality.api2db.fetchunif.fetchunif as unif
# import airquality.database.rec.
import airquality.looper.datelooper as dlp


class FetchCommand(base.Command):

    ################################ __init__ ###############################
    def __init__(
            self,
            fw: apiwrp.FetchWrapper,
            iw: ins.MobileMeasureInsertWrapper,
            sw: Union[mbsel.MobileSelectWrapper, stsel.StationSelectWrapper],
            urb: unif.FetchUniformResponseBuilder,
            dtlpc=dlp.DateLooper,
            # rb:
            log_filename="log"
    ):
        super(FetchCommand, self).__init__(fw=fw, iw=iw, log_filename=log_filename)
        self.date_looper_class = dtlpc
        self.select_wrapper = sw
        self.uniform_response_builder = urb

    ################################ execute ###############################
    @log_decorator.log_decorator()
    def execute(self):

        # Query sensor ids from database
        db_responses = self.select_wrapper.select()
        if not db_responses:
            self.log_warning(f"{FetchCommand.__name__}: no sensor found inside the database => no measure inserted")
            return

        for response in db_responses:
            for channel in response.api_param:

                last_acquisition = channel.last_acquisition
                self.log_info(f"{FetchCommand.__name__}: last acquisition => {last_acquisition.get_formatted_timestamp()}")

                # self.url_builder.with_api_key()

                # URL BUILDER => build url

                # Pass URL to FetchWrapper

                date_looper = self.date_looper_class(
                    fw = self.fetch_wrapper,
                    strt = last_acquisition,
                    stp = ts.CurrentTimestamp(),
                    log_filename = self.log_filename
                )
                date_looper.set_file_logger(self.file_logger)
                date_looper.set_console_logger(self.console_logger)

                while date_looper.has_next():

                    api_responses = date_looper.get_next_api_responses()
                    if not api_responses:
                        self.log_warning(f"{FetchCommand.__name__}: empty API sensor data => continue")
                        continue


# ############################# FUNCTION 3 ##############################
# @log_decorator.log_decorator()
# def _uniform_filter_insert(self,
#                            sensor_data_flt: flt.BaseFilter,
#                            sensor_id: int,
#                            channel_name: str,
#                            sensor_data: List[Dict[str, Any]]
#                            ):
#
#     # Uniform sensor data
#     uniformed_sensor_data = [self.api2db_adapter.raw2container(data) for data in sensor_data]
#
#     # Filter measure to keep only new measurements
#     new_data = [data for data in uniformed_sensor_data if sensor_data_flt.filter(data)]
#
#     # Log message
#     self.log_info(f"{FetchCommand.__name__}: found {len(new_data)}/{len(uniformed_sensor_data)} new measurements")
#     if not new_data:
#         return
#
#     # Insert measurements
#     self.insert_wrapper.insert(sensor_data=new_data, sensor_id=sensor_id, sensor_channel=channel_name)
