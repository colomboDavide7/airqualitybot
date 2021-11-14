#################################################
#
# @Author: davidecolombo
# @Date: mer, 27-10-2021, 11:33
# @Description: this script defines the bot classes for the fetch module
#
#################################################
import airquality.bot.base as base
import airquality.logger.decorator as log_decorator
import airquality.api.fetch as api
import airquality.database.conn as db
import airquality.database.util.datatype.timestamp as ts
import airquality.bot.util.datelooper as loop
import airquality.bot.util.executor as ex


class FetchBot(base.BaseBot):

    def __init__(self, sensor_type: str, dbconn: db.DatabaseAdapter):
        super(FetchBot, self).__init__(sensor_type=sensor_type, dbconn=dbconn)
        self.date_looper_cls = None
        self.sensor_query_executor = None
        self.bot_query_executor = None

    def add_date_looper_class(self, date_looper_class: loop.DateLooper):
        self.date_looper_cls = date_looper_class

    def add_sensor_query_executor(self, executor: ex.SensorQueryExecutor):
        self.sensor_query_executor = executor

    def add_bot_query_executor(self, executor: ex.BotQueryExecutor):
        self.bot_query_executor = executor

    @log_decorator.log_decorator()
    def run(self):

        sensor_ids = self.bot_query_executor.get_sensor_id()
        if not sensor_ids:
            self.debugger.warning(f"no sensor found for type='{self.sensor_type}' => done")
            self.logger.warning(f"no sensor found for type='{self.sensor_type}' => done")
            return

        measure_param_map = self.bot_query_executor.get_measure_param()
        if not measure_param_map:
            raise SystemExit(f"bad database answer => empty 'measure_param' for type='{self.sensor_type}'")

        ############################# CYCLE ON ALL SENSOR IDS FOUND ##############################
        for sensor_id in sensor_ids:

            db_api_param = self.sensor_query_executor.get_sensor_api_param(sensor_id)
            uniformed_param = self.param_rshp_class(db_api_param).reshape()

            ############################# CYCLE ON UNIFORMED API PARAM OF A SINGLE SENSOR ##############################
            for api_param in uniformed_param:

                # Pop the channel name from the uniformed api param of the given sensor_id
                ch_name = api_param.pop('channel_name')
                self.debugger.info(f"start fetch new measurements on channel='{ch_name}' for sensor_id={sensor_id}")
                self.logger.info(f"start fetch new measurements on channel='{ch_name}' for sensor_id={sensor_id}")

                # Add database 'api_param' to URLBuilder
                self.url_builder.url_param.update(api_param)

                # Query sensor channel last acquisition
                last_acquisition = self.sensor_query_executor.get_last_acquisition(channel=ch_name, sensor_id=sensor_id)
                filter_timestamp = ts.SQLTimestamp(last_acquisition)
                start_ts = filter_timestamp
                stop_ts = ts.CurrentTimestamp()

                # Create date looper
                looper = self.date_looper_cls(self.url_builder, start_ts = start_ts, stop_ts = stop_ts)

                # Cycle until looper has no more URL
                while looper.has_next():

                    url = looper.get_next_url()
                    raw_api_packets = api.fetch(url)
                    parsed_api_packets = self.text_parser_class(raw_api_packets).parse()
                    api_data = self.api_extr_class(parsed_api_packets, channel_name=ch_name).extract()
                    if not api_data:
                        self.debugger.info(f"empty API answer on channel='{ch_name}' for sensor_id={sensor_id}")
                        self.logger.info(f"empty API answer on channel='{ch_name}' for sensor_id={sensor_id}")
                        continue

                    ############################# UNIFORM PACKETS FOR SQL BUILDER ##############################
                    uniformed_packets = []
                    for data in api_data:
                        uniformed_packets.append(self.measure_rshp_class(data).reshape())

                    # Remove packets already present into the database
                    fetched_new_measures = []
                    for packet in uniformed_packets:
                        timestamp = self.timest_cls(packet['timestamp'])
                        if timestamp.is_after(filter_timestamp):
                            fetched_new_measures.append(packet)

                    # Continue to the next 'sensor_id' if there are no new measurements
                    if not fetched_new_measures:
                        self.debugger.warning(f"no new measurements for sensor_id={sensor_id}")
                        self.logger.warning(f"no new measurements for sensor_id={sensor_id}")
                        continue

                    # Debug and log new measurement timestamp range
                    first_timestamp = fetched_new_measures[0]['timestamp']
                    last_timestamp = fetched_new_measures[-1]['timestamp']
                    self.debugger.info(f"found new measurements from {first_timestamp} to {last_timestamp}")
                    self.logger.info(f"found new measurements from {first_timestamp} to {last_timestamp}")

                    # Add new measurements
                    for fetched_new_measure in fetched_new_measures:
                        pass

                    self.debugger.info(f"end fetch new measurements on channel={ch_name} for sensor_id={sensor_id}")
                    self.logger.info(f"end fetch new measurements on channel={ch_name} for sensor_id={sensor_id}")

        ################################ SAFELY CLOSE DATABASE CONNECTION ################################
        self.debugger.info("new measurement(s) successfully fetched => done")
        self.logger.info("new measurement(s) successfully fetched => done")
