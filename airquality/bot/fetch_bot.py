#################################################
#
# @Author: davidecolombo
# @Date: mer, 27-10-2021, 11:33
# @Description: this script defines the bot classes for the fetch module
#
#################################################
from typing import Dict, Any, List

# IMPORT MODULES
import logging
import airquality.io.remote.api.adapter as api
import airquality.io.remote.database.adapter as db
import airquality.utility.picker.query as pk
import airquality.utility.parser.file as fp
import airquality.data.builder.timest as ts
import airquality.data.reshaper.packet as rshp
import airquality.data.reshaper.uniform.api2db as a2d
import airquality.data.reshaper.uniform.db2api as d2a

# IMPORT CONSTANTS
import airquality.core.constants.system_constants as sc
from airquality.core.constants.shared_constants import DEBUG_HEADER, INFO_HEADER, WARNING_HEADER

################################ FETCH LOGGER ################################
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler(filename='log/fetch.log', mode='a')
formatter = logging.Formatter('[%(levelname)s] - %(asctime)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


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
                 url_builder_class=None):

        self.dbconn = dbconn
        self.timest_fmt = timest_fmt
        self.file_parser = file_parser
        self.query_picker = query_picker
        self.packet_reshaper = packet_reshaper
        self.db2api_reshaper = db2api_reshaper
        self.api2db_reshaper = api2db_reshaper
        self.url_builder_class = url_builder_class

    ################################ RUN METHOD ################################
    def run(self, api_address: str, url_param: Dict[str, Any], sensor_ids: List[int]):

        last_acquisition_ts = ts.SQLTimestamp("2021-11-08 20:00:00")

        for sensor_id in sensor_ids:
            print(20 * "=" + f" {sensor_id} " + 20 * '=')

            query = self.query_picker.select_api_param_from_sensor_id(sensor_id)
            answer = self.dbconn.send(query)
            api_param = dict(answer)
            uniformed_param = self.db2api_reshaper.db2api(api_param)

            ############################# BUILD URL AND FETCH DATA ##############################
            for param in uniformed_param:
                print(f"{INFO_HEADER} channel={param['channel_name']}")
                self.packet_reshaper.ch_name = param.pop('channel_name')
                tmp_url_param = url_param.copy()
                tmp_url_param.update(param)
                url_builder = self.url_builder_class(api_address=api_address, parameters=tmp_url_param)
                url = url_builder.url()
                print(f"{INFO_HEADER} {url}")

                ############################# RESHAPE PACKETS ##############################
                raw_api_packets = api.UrllibAdapter.fetch(url)
                parsed_api_packets = self.file_parser.parse(raw_api_packets)
                reshaped_packets = self.packet_reshaper.reshape(parsed_api_packets)
                if not reshaped_packets:
                    msg = f"empty API answer for id={sensor_id}"
                    print(f"{INFO_HEADER} msg")
                    logger.info(msg)
                    continue

                ############################# UNIFORM PACKETS FOR SQL BUILDER ##############################
                uniformed_packets = []
                for packet in reshaped_packets:
                    uniformed_packets.append(self.api2db_reshaper.api2db(packet))

                print(20 * "=" + " FILTER FETCHED MEASUREMENTS " + 20 * '=')
                filtered_packets = []
                for packet in uniformed_packets:
                    timestamp = ts.SQLTimestamp(packet['timestamp'], fmt=self.timest_fmt)
                    if timestamp.is_after(last_acquisition_ts):
                        filtered_packets.append(packet)
                    else:
                        print(f"{WARNING_HEADER} '{packet['timestamp']}' => old measure")

                if not filtered_packets:
                    msg = f"no new measurements for id={sensor_id}"
                    print(f"{INFO_HEADER} {msg}")
                    logger.info(msg)
                    continue

                ############################# PRINT ONLY NEW MEASUREMENTS ##############################
                print(20 * "=" + " NEW MEASUREMENTS FETCHED " + 20 * '=')
                if sc.DEBUG_MODE:
                    for packet in filtered_packets:
                        print(f"{DEBUG_HEADER} timestamp={packet['timestamp']}")

        ################################ SAFELY CLOSE DATABASE CONNECTION ################################
        logger.info("new measurement(s) successfully fetched => done")
        self.dbconn.close_conn()
