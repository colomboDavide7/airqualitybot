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


class FetchBot(base.BaseBot):

    def __init__(self, sensor_type: str, dbconn: db.DatabaseAdapter):
        super(FetchBot, self).__init__(sensor_type=sensor_type, dbconn=dbconn)

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

        # Query the 'param_code, param_id' tuples for inserting measurements
        query = self.query_picker.select_measure_param_from_sensor_type(self.sensor_type)
        answer = self.dbconn.send(query)
        measure_param_map = dict(answer)

        if not measure_param_map:
            raise SystemExit(f"bad database answer => empty 'measure_param' for type='{self.sensor_type}'")

        ############################# CYCLE ON ALL SENSOR IDS FOUND ##############################
        for sensor_id in sensor_ids:

            # Select database API param
            query = self.query_picker.select_api_param_from_sensor_id(sensor_id)
            answer = self.dbconn.send(query)
            db_api_param = dict(answer)
            uniformed_param = self.param_rshp_class(db_api_param).reshape()

            ############################# CYCLE ON UNIFORMED API PARAM OF A SINGLE SENSOR ##############################
            for api_param in uniformed_param:

                # Pop the channel name from the uniformed api param of the given sensor_id
                ch_name = api_param.pop('channel_name')
                self.debugger.info(f"start fetch new measurements on channel='{ch_name}' for sensor_id={sensor_id}")
                self.logger.info(f"start fetch new measurements on channel='{ch_name}' for sensor_id={sensor_id}")

                # Get last acquisition timestamp to filter out old measurements
                query = self.query_picker.select_last_acquisition(channel=ch_name, sensor_id=sensor_id)
                answer = self.dbconn.send(query)
                if not answer:
                    raise SystemExit(f"bad database answer => empty 'last_acquisition' for sensor_id={sensor_id} and"
                                     f" channel_name='{ch_name}'")

                # Extract last acquisition timestamp
                last_acquisition_ts = ts.SQLTimestamp(str(answer[0][0]))

                # Define stop timestamp as the moment in which the program is ran
                stop_ts = ts.CurrentTimestamp()

                while stop_ts.is_after(last_acquisition_ts):

                    date_param = {}
                    if self.sensor_type == 'thingspeak':
                        date_param['start'] = last_acquisition_ts.ts.replace(" ", "%20")
                        date_param['end'] = last_acquisition_ts.add_days(days=7).ts.replace(" ", "%20")
                        self.debugger.info(f"start_at={date_param['start']} - end_at={date_param['end']}")
                    elif self.sensor_type == 'atmotube':
                        timestamp = last_acquisition_ts.ts
                        date, time = timestamp.split(" ")
                        date_param['date'] = date
                        self.debugger.info(f"start_at={date_param['date']}")

                    # Update URLBuilder parameters
                    self.url_builder.update_param(api_param)                # add database api param
                    self.url_builder.update_param(date_param)               # add date api param
                    url = self.url_builder.url()
                    raw_api_packets = api.fetch(url)
                    parsed_api_packets = self.text_parser_class(raw_api_packets).parse()
                    api_data = self.api_extr_class(parsed_api_packets, channel_name=ch_name).extract()
                    if not api_data:
                        self.debugger.info(f"empty API answer on channel='{ch_name}' for sensor_id={sensor_id}")
                        self.logger.info(f"empty API answer on channel='{ch_name}' for sensor_id={sensor_id}")

                        if self.sensor_type == 'thingspeak':
                            last_acquisition_ts = last_acquisition_ts.add_days(7)
                        elif self.sensor_type == 'atmotube':
                            last_acquisition_ts = last_acquisition_ts.add_days(1)
                        continue

                    ############################# UNIFORM PACKETS FOR SQL BUILDER ##############################
                    uniformed_packets = []
                    for data in api_data:
                        uniformed_packets.append(self.measure_rshp_class(data).reshape())

                    # Remove packets already present into the database
                    fetched_new_measures = []
                    for packet in uniformed_packets:
                        timestamp = self.timest_cls(packet['timestamp'])
                        if timestamp.is_after(last_acquisition_ts):
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

                    if self.sensor_type == 'thingspeak':
                        last_acquisition_ts = last_acquisition_ts.add_days(7)
                    elif self.sensor_type == 'atmotube':
                        last_acquisition_ts = last_acquisition_ts.add_days(1)

        ################################ SAFELY CLOSE DATABASE CONNECTION ################################
        self.debugger.info("new measurement(s) successfully fetched => done")
        self.logger.info("new measurement(s) successfully fetched => done")

# from_datetime = DatetimeParser.string2datetime("2018-01-01 00:00:00")  # [ONLY FOR NOW]
#
# from_datetime = DatetimeParser.string2datetime(datetime_string=channel_param['channel_ts']['val'])
# from_datetime = DatetimeParser.add_seconds_to_datetime(ts=from_datetime, seconds=3)
#
# # define to datetime
# to_datetime = DatetimeParser.add_days_to_datetime(ts=from_datetime, days=7)
#
# if (to_datetime - stop_datetime).total_seconds() > 0:
#     to_datetime = stop_datetime
#
# # CONTINUE UNTIL TODAY IS REACHED
# while (stop_datetime - from_datetime).total_seconds() >= 0:
#
