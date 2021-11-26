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
import airquality.api.url.dynurl as url
import airquality.api.url.timedecor as urldec
import airquality.database.op.ins.mbmeasins as ins
import airquality.database.op.sel.mobilesel as mbsel
import airquality.database.op.sel.stationsel as stsel
import types.timestamp as ts
import airquality.database.rec.mbmeasrec as mbrec
import airquality.database.rec.stmeasrec as strec
import airquality.api2db.adptype as adptype


class FetchCommand(base.Command):

    ################################ __init__ ###############################
    def __init__(
            self,
            tud: urldec.URLTimeDecorator,
            ub: url.DynamicURLBuilder,
            ara: adptype.Measure,
            fw: apiwrp.FetchWrapper,
            iw: ins.MobileMeasureInsertWrapper,
            sw: Union[mbsel.MobileSelectWrapper, stsel.StationSelectWrapper],
            rb_cls=Union[mbrec.MobileMeasureRecord, strec.StationMeasureRecord],
            log_filename="log"
    ):
        super(FetchCommand, self).__init__(ub=ub, fw=fw, log_filename=log_filename)
        self.url_builder = ub
        self.api_resp_adpt = ara
        self.insert_wrapper = iw
        self.select_wrapper = sw
        self.record_class = rb_cls
        self.time_url_decorator = tud

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

                # Set mandated parameters
                self.url_builder.with_identifier(channel.ch_id).with_api_key(channel.ch_key)

                # Set start and stop time range
                self.time_url_decorator.with_start_ts(start=last_acquisition).with_stop_ts(ts.CurrentTimestamp())

                while self.time_url_decorator.has_next_date():
                    # Fetch API data
                    api_responses = self.fetch_wrapper.fetch(url=self.time_url_decorator.build())
                    if not api_responses:
                        self.log_warning(f"{FetchCommand.__name__}: empty API sensor data => continue")
                        continue

                    # if api_responses[0].

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
