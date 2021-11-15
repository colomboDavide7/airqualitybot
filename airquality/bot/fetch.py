#################################################
#
# @Author: davidecolombo
# @Date: mer, 27-10-2021, 11:33
# @Description: this script defines the bot classes for the fetch module
#
#################################################
import airquality.bot.base as base
import airquality.api.util.request as api
import airquality.database.util.datatype.timestamp as ts
import airquality.bot.util.datelooper as loop
import airquality.database.operation.select as select_op


################################ FETCH BOT ################################
class FetchBot(base.BaseBot):

    def __init__(self):
        super(FetchBot, self).__init__()
        self.date_looper_cls = None
        self.id_executor = None

    def add_date_looper_class(self, date_looper_class: loop.DateLooper):
        self.date_looper_cls = date_looper_class

    def add_sensor_id_select_wrapper(self, op: select_op.SensorIDSelectWrapper):
        self.id_executor = op

    ################################ RUN METHOD ################################
    def execute(self):

        sensor_ids = self.sensor_type_select_wrapper.get_sensor_id()
        if not sensor_ids:
            self.debugger.warning(f"no sensor found => done")
            self.logger.warning(f"no sensor found => done")
            return

        measure_param_map = self.sensor_type_select_wrapper.get_measure_param()
        if not measure_param_map:
            raise SystemExit(f"bad database answer => empty 'measure_param'")

        ############################# CYCLE ON ALL SENSOR IDS FOUND ##############################
        for sensor_id in sensor_ids:

            # Extract database API parameters
            db_api_param = self.id_executor.get_sensor_api_param(sensor_id)
            uniformed_param = self.db2api_adapter(db_api_param).reshape()

            ############################# CYCLE ON UNIFORMED API PARAM OF A SINGLE SENSOR ##############################
            for api_param in uniformed_param:

                # Pop the channel name from the uniformed api param of the given sensor_id
                ch_name = api_param.pop('channel_name')
                self.debugger.info(f"start fetch new measurements on channel='{ch_name}' for sensor_id={sensor_id}")
                self.logger.info(f"start fetch new measurements on channel='{ch_name}' for sensor_id={sensor_id}")

                # Add database 'api_param' to URLBuilder
                self.url_builder.url_param.update(api_param)

                # Query sensor channel last acquisition
                last_acquisition = self.id_executor.get_last_acquisition(channel=ch_name, sensor_id=sensor_id)
                filter_timestamp = ts.SQLTimestamp(last_acquisition)
                start_ts = filter_timestamp
                stop_ts = ts.CurrentTimestamp()

                # Create date looper
                looper = self.date_looper_cls(self.url_builder, start_ts = start_ts, stop_ts = stop_ts)

                # Cycle until looper has no more URL
                while looper.has_next():

                    # Fetch data from API
                    url = looper.get_next_url()
                    raw_api_packets = api.fetch(url)
                    parsed_api_packets = self.text_parser(raw_api_packets).parse()
                    api_data = self.api_extr_class(parsed_api_packets, channel_name=ch_name).extract()
                    if not api_data:
                        self.debugger.info(f"empty API answer on channel='{ch_name}' for sensor_id={sensor_id}")
                        self.logger.info(f"empty API answer on channel='{ch_name}' for sensor_id={sensor_id}")
                        continue

                    ############################# UNIFORM PACKETS FOR SQL BUILDER ##############################
                    uniformed_packets = []
                    for data in api_data:
                        uniformed_packets.append(self.measure_adapter.reshape(data))

                    # Set 'filter_ts' dependency
                    self.packet_filter.set_filter_ts(filter_timestamp)

                    # Filter measure to keep only new measurements
                    fetched_new_measurements = self.packet_filter.filter(uniformed_packets)
                    if not fetched_new_measurements:
                        self.debugger.warning(f"no new measurements for sensor_id={sensor_id}")
                        self.logger.warning(f"no new measurements for sensor_id={sensor_id}")
                        continue

                    # Add new measurements
                    # self.insertion_executor.insert_measurements(fetched_new_measurements)

                    self.debugger.info(f"end fetch new measurements on channel={ch_name} for sensor_id={sensor_id}")
                    self.logger.info(f"end fetch new measurements on channel={ch_name} for sensor_id={sensor_id}")

        ################################ SAFELY CLOSE DATABASE CONNECTION ################################
        self.debugger.info("new measurement(s) successfully fetched => done")
        self.logger.info("new measurement(s) successfully fetched => done")
