#################################################
#
# @Author: davidecolombo
# @Date: mer, 27-10-2021, 11:33
# @Description: this script defines the bot classes for the fetch module
#
#################################################
from typing import Dict, Any, List

# IMPORT MODULES
import airquality.core.logger.log as log
import airquality.core.logger.decorator as log_decorator
import airquality.io.remote.api.adapter as api
import airquality.io.remote.database.adapter as db
import airquality.utility.picker.query as pk
import airquality.utility.parser.file as fp
import airquality.data.builder.timest as ts
import airquality.data.reshaper.packet as rshp
import airquality.data.reshaper.uniform.api2db as a2d
import airquality.data.reshaper.uniform.db2api as d2a


################################ FETCH BOT ################################
class FetchBot:

    def __init__(self,
                 timest_fmt: str,
                 dbconn: db.DatabaseAdapter,
                 file_parser: fp.FileParser,
                 query_picker: pk.QueryPicker,
                 packet_reshaper: rshp.PacketReshaper,
                 api2db_reshaper: a2d.UniformReshaper,
                 db2api_reshaper: d2a.UniformReshaper,
                 url_builder_class=None,
                 log_filename='fetch',
                 log_sub_dir='log'):

        self.dbconn = dbconn
        self.timest_fmt = timest_fmt
        self.file_parser = file_parser
        self.query_picker = query_picker
        self.packet_reshaper = packet_reshaper
        self.db2api_reshaper = db2api_reshaper
        self.api2db_reshaper = api2db_reshaper
        self.url_builder_class = url_builder_class
        self.log_filename = log_filename
        self.log_sub_dir = log_sub_dir
        self.logger = log.get_logger(log_filename=log_filename, log_sub_dir=log_sub_dir)
        self.debugger = log.get_logger(use_color=True)

    ################################ RUN METHOD ################################
    @log_decorator.log_decorator()
    def run(self, api_address: str, opt_url_param: Dict[str, Any], sensor_ids: List[int]):

        last_acquisition_ts = ts.SQLTimestamp("2021-11-10 01:00:00")

        for sensor_id in sensor_ids:
            # Select api param from database
            query = self.query_picker.select_api_param_from_sensor_id(sensor_id)
            answer = self.dbconn.send(query)
            db_api_param = dict(answer)
            uniformed_param = self.db2api_reshaper.db2api(db_api_param)

            ############################# CYCLE ON UNIFORMED API PARAM OF A SINGLE SENSOR ##############################
            for api_param in uniformed_param:

                # Pop the channel name from the uniformed api param of the given sensor_id
                ch_name = api_param.pop('channel_name')
                self.debugger.info(f"start fetch new measurements on channel={ch_name} for sensor_id={sensor_id}")
                self.logger.info(f"start fetch new measurements on channel={ch_name} for sensor_id={sensor_id}")

                # Set the packet_reshaper 'ch_name' property
                self.packet_reshaper.ch_name = ch_name

                # Merge bot 'url_param' (coming from API file) and 'param' (coming from database)
                url_param = opt_url_param.copy()
                url_param.update(api_param)
                self.debugger.debug(', '.join(f"{k}={v!r}" for k, v in url_param.items()))
                self.logger.debug(', '.join(f"{k}={v!r}" for k, v in url_param.items()))

                # Make 'url_builder' and build 'url'
                url_builder = self.url_builder_class(api_address=api_address, parameters=url_param)
                url = url_builder.url()
                self.debugger.info(url)
                self.logger.info(url)

                ############################# RESHAPE PACKETS ##############################
                raw_api_packets = api.UrllibAdapter.fetch(url)
                parsed_api_packets = self.file_parser.parse(raw_api_packets)
                reshaped_packets = self.packet_reshaper.reshape(parsed_api_packets)
                if not reshaped_packets:
                    self.debugger.info(f"empty API answer for sensor_id={sensor_id}")
                    self.logger.info(f"empty API answer for sensor_id={sensor_id}")
                    continue

                ############################# UNIFORM PACKETS FOR SQL BUILDER ##############################
                uniformed_packets = []
                for packet in reshaped_packets:
                    uniformed_packets.append(self.api2db_reshaper.api2db(packet))

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
        self.dbconn.close_conn()
