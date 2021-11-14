#################################################
#
# @Author: davidecolombo
# @Date: gio, 28-10-2021, 08:30
# @Description: this script contains the classes for initializing the database with different sensor's data.
#
#################################################
import airquality.bot.base as base
import airquality.logger.decorator as log_decorator
import airquality.api.fetch as api
import airquality.database.conn as db
import airquality.database.util.sql.record as rec


################################ INITIALIZE BOT ################################
class InitializeBot(base.BaseBot):

    def __init__(self, sensor_type: str, dbconn: db.DatabaseAdapter):
        super(InitializeBot, self).__init__(sensor_type=sensor_type, dbconn=dbconn)

    @log_decorator.log_decorator()
    def run(self):

        # Select database 'sensor_names'
        query = self.query_picker.select_sensor_names_from_sensor_type(self.sensor_type)
        answer = self.dbconn.send(query=query)
        database_sensor_names = [t[0] for t in answer]

        # Build URL
        url = self.url_builder.url()
        raw_packets = api.fetch(url)
        parsed_packets = self.text_parser_class(raw_packets).parse()
        api_data = self.api_extr_class(parsed_packets).extract()

        if not api_data:
            self.debugger.warning("empty API answer => done")
            self.logger.warning("empty API answer => done")
            return

        # Reshape API data
        uniformed_packets = []
        for fetched_new_sensor in api_data:
            uniformed_packets.append(self.sensor_rshp_class(fetched_new_sensor).reshape())

        # Remove fetched sensors that are already present into the database
        fetched_new_sensors = []
        for uniformed_packet in uniformed_packets:
            if uniformed_packet['name'] not in database_sensor_names:
                fetched_new_sensors.append(uniformed_packet)
                self.debugger.info(f"found new sensor '{uniformed_packet['name']}'")
                self.logger.info(f"found new sensor '{uniformed_packet['name']}'")
            else:
                self.debugger.warning(f"skip sensor '{uniformed_packet['name']}' => already present")
                self.logger.warning(f"skip sensor '{uniformed_packet['name']}' => already present")

        if not fetched_new_sensors:
            self.debugger.info("all sensors are already present into the database => done")
            self.logger.info("all sensors are already present into the database => done")
            return

        # Query the max 'sensor_id' for knowing the 'sensor_id' during the insertion
        query = self.query_picker.select_max_sensor_id()
        answer = self.dbconn.send(query)
        max_sensor_id = [t[0] for t in answer]

        ####################### DEFINE THE FIRST SENSOR ID FROM WHERE TO START ########################
        starting_new_sensor_id = 1
        if max_sensor_id[0] is not None:
            starting_new_sensor_id = max_sensor_id[0] + 1
            msg = f"found database sensor_id={max_sensor_id[0]!s} => new insertion starts at: {starting_new_sensor_id!s}"
            self.debugger.info(msg)
            self.logger.info(msg)

        ############################## BUILD SQL FROM FILTERED UNIFORMED PACKETS #############################
        location_values = []
        api_param_values = []
        sensor_values = []
        sensor_info_values = []
        for fetched_new_sensor in fetched_new_sensors:
            # **************************
            sensor_value = rec.SensorRecord(sensor_id=starting_new_sensor_id, packet=fetched_new_sensor)
            sensor_values.append(sensor_value)
            # **************************
            geometry = self.geom_builder_class(packet=fetched_new_sensor)
            valid_from = self.current_ts.ts
            geom = geometry.geom_from_text()
            geom_value = rec.LocationRecord(sensor_id=starting_new_sensor_id, valid_from=valid_from, geom=geom)
            location_values.append(geom_value)
            # **************************
            api_param_value = rec.APIParamRecord(sensor_id=starting_new_sensor_id, packet=fetched_new_sensor)
            api_param_values.append(api_param_value)
            # **************************
            sensor_info_value = rec.SensorInfoRecord(sensor_id=starting_new_sensor_id, packet=fetched_new_sensor)
            sensor_info_value.add_timest_class(timest_cls=self.timest_cls)
            sensor_info_values.append(sensor_info_value)
            # **************************
            starting_new_sensor_id += 1

        ################################ BUILD + EXECUTE QUERIES ################################
        query = self.query_picker.initialize_sensors(
            sensor_values=sensor_values,
            api_param_values=api_param_values,
            location_values=location_values,
            sensor_info_values=sensor_info_values
        )
        self.dbconn.send(query)

        self.debugger.info("new sensor(s) successfully inserted => done")
        self.logger.info("new sensor(s) successfully inserted => done")
