#################################################
#
# @Author: davidecolombo
# @Date: mer, 27-10-2021, 11:33
# @Description: this script defines the bot classes for the fetch module
#
#################################################

# IMPORT MODULES
import airquality.bot.base as base
import airquality.core.logger.log as log
import airquality.core.logger.decorator as log_decorator
import airquality.io.remote.api.adapter as api
import airquality.io.remote.database.adapter as db
import airquality.data.builder.timest as ts


################################ FETCH BOT ################################
class FetchBot(base.BaseBot):

    def __init__(self, sensor_type: str, dbconn: db.DatabaseAdapter, log_filename='fetch', log_sub_dir='log'):
        super(FetchBot, self).__init__(sensor_type=sensor_type, dbconn=dbconn)
        self.log_filename = log_filename
        self.log_sub_dir = log_sub_dir
        self.logger = log.get_logger(log_filename=log_filename, log_sub_dir=log_sub_dir)
        self.debugger = log.get_logger(use_color=True)

    ################################ RUN METHOD ################################
    @log_decorator.log_decorator()
    def run(self):

        # Query 'sensor_ids' of the given 'sensor_type'
        query = self.query_picker.select_sensor_ids_from_sensor_type(self.sensor_type)
        answer = self.dbconn.send(query=query)
        sensor_ids = [t[0] for t in answer]

        if not sensor_ids:
            self.debugger.warning(f"no sensor found for type='{self.sensor_type}' => done")
            self.logger.warning(f"no sensor found for type='{self.sensor_type}' => done")
            return

        last_acquisition_ts = ts.SQLTimestamp("2021-11-10 01:00:00")

        for sensor_id in sensor_ids:
            # Select api param from database
            query = self.query_picker.select_api_param_from_sensor_id(sensor_id)
            answer = self.dbconn.send(query)
            db_api_param = dict(answer)
            uniformed_param = self.db2api_rshp_class(db_api_param).reshape()

            ############################# CYCLE ON UNIFORMED API PARAM OF A SINGLE SENSOR ##############################
            for api_param in uniformed_param:

                # Pop the channel name from the uniformed api param of the given sensor_id
                ch_name = api_param.pop('channel_name')
                self.debugger.info(f"start fetch new measurements on channel={ch_name} for sensor_id={sensor_id}")
                self.logger.info(f"start fetch new measurements on channel={ch_name} for sensor_id={sensor_id}")

                # Update URLBuilder parameters
                self.url_builder.update_param(api_param)

                # Build URL
                url = self.url_builder.url()
                self.debugger.info(url)
                self.logger.info(url)

                # Fetch API data
                raw_api_packets = api.fetch(url)
                parsed_api_packets = self.text_parser_class(raw_api_packets).parse()
                api_data = self.api_extr_class(parsed_api_packets, channel_name=ch_name).extract()
                if not api_data:
                    self.debugger.info(f"empty API answer for sensor_id={sensor_id}")
                    self.logger.info(f"empty API answer for sensor_id={sensor_id}")
                    continue

                ############################# UNIFORM PACKETS FOR SQL BUILDER ##############################
                uniformed_packets = []
                for data in api_data:
                    uniformed_packets.append(self.api2db_rshp_class(data).reshape())

                # Remove packets already present into the database
                fetched_new_measures = []
                for packet in uniformed_packets:
                    timestamp = ts.SQLTimestamp(packet['timestamp'], fmt=self.timest_fmt)
                    if timestamp.is_after(last_acquisition_ts):
                        fetched_new_measures.append(packet)

                # Continue to the next 'sensor_id' if there are no new measurements
                if not fetched_new_measures:
                    self.debugger.debug(f"no new measurements for sensor_id={sensor_id}")
                    self.logger.info(f"no new measurements for sensor_id={sensor_id}")
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
