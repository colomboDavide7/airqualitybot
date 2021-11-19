#################################################
#
# @Author: davidecolombo
# @Date: mer, 27-10-2021, 11:33
# @Description: this script defines the bot classes for the fetch module
#
#################################################
import airquality.bot.base as base
import airquality.database.util.datatype.timestamp as ts
import airquality.database.operation.select.type as select
import airquality.adapter.config as adapt_const


################################ FETCH BOT ################################
class FetchBot(base.BaseBot):

    def __init__(self):
        super(FetchBot, self).__init__()
        self.date_looper_class = None
        self.sensor_id_select_wrapper = None

    def add_date_looper_class(self, looper_class):
        self.date_looper_class = looper_class

    def add_sensor_id_select_wrapper(self, wrapper: select.SensorIDSelectWrapper):
        self.sensor_id_select_wrapper = wrapper

    def _exit_on_missing_external_dependencies(self):
        if self.sensor_id_select_wrapper is None:
            raise SystemExit(f"{FetchBot.__name__}: bad setup => missing external dependency 'sensor_id_select_wrapper'")
        if self.date_looper_class is None:
            raise SystemExit(f"{FetchBot.__name__}: bad setup => missing external dependency 'date_looper_class'")

    ################################ EXECUTE METHOD ################################
    def execute(self):

        self.log_info(f"{FetchBot.__name__}: begin execution...")
        self._exit_on_missing_external_dependencies()

        sensor_ids = self.sensor_type_select_wrapper.get_sensor_id()
        if not sensor_ids:
            self.console_logger.warning(f"no sensor found => done")
            self.file_logger.warning(f"no sensor found => done")
            return

        ############################# CYCLE ON ALL SENSOR IDS FOUND ##############################
        for sensor_id in sensor_ids:

            self.log_info(20*"*" + f"sensor_id={sensor_id}" + 20*"*")

            # Extract database API parameters
            db_api_param = self.sensor_id_select_wrapper.get_sensor_api_param(sensor_id)
            uniformed_param = self.db2api_adapter.reshape(db_api_param)

            ############################# CYCLE ON UNIFORMED API PARAM OF A SINGLE SENSOR ##############################
            for api_param in uniformed_param:

                # Pop the channel name from the uniformed api param of the given sensor_id
                ch_name = api_param.pop(adapt_const.CH_NAME)
                self.log_info(20*"%" + f"channel_name={ch_name}" + 20*"%")

                # Query sensor channel last acquisition
                last_acquisition = self.sensor_id_select_wrapper.get_last_acquisition(channel=ch_name, sensor_id=sensor_id)
                filter_timestamp = ts.SQLTimestamp(last_acquisition)
                self.log_info(f"...last acquisition was at => {filter_timestamp.ts}")

                # DateLooper
                looper = self.date_looper_class(self.fetch_wrapper, start_ts=filter_timestamp, stop_ts=ts.CurrentTimestamp())
                looper.set_file_logger(self.file_logger)
                looper.set_console_logger(self.console_logger)

                ############################# UNIFORM PACKETS FOR SQL BUILDER ##############################
                while looper.has_next():

                    # Update both URL param and Channel name by adding those specific for the current sensor
                    looper.update_url_param(api_param)
                    looper.set_channel_name(ch_name)

                    # Fetch data from API
                    sensor_data = looper.get_next_sensor_data()
                    if not sensor_data:
                        self.log_warning("continue => empty API sensor data")
                        continue

                    # Uniform sensor data
                    uniformed_sensor_data = [self.api2db_adapter.reshape(data) for data in sensor_data]

                    # Set 'filter_ts' dependency
                    self.sensor_data_filter.set_filter_ts(filter_timestamp)

                    # Filter measure to keep only new measurements
                    new_data = [data for data in uniformed_sensor_data if self.sensor_data_filter.filter(data)]
                    n_tot = len(uniformed_sensor_data)
                    n_filtered = len(new_data)
                    self.log_info(f"...found {n_filtered}/{n_tot} new measurements...")

                    if not new_data:
                        self.log_info(f"continue => no new measurements")
                        continue

                    # Add new measurements
                    self.insert_wrapper.insert_measurements(sensor_data=new_data, sensor_id=sensor_id, channel=ch_name)

        self.log_info(f"{FetchBot.__name__}: done => new measurements successfully inserted")
