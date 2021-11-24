######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 17:53
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import airquality.command.fetch.fetch as command
import airquality.command.config as comm_const
import airquality.command.setup as setup

import airquality.logger.util.decorator as log_decorator

import airquality.file.util.parser as fp
import airquality.file.util.loader as fl

import airquality.api.util.extractor as extr
import airquality.api.util.url as url

import airquality.database.operation.select.sensor as sel_type
import database.record.georec as loc
import airquality.database.operation.insert.fetchoprt as ins
import database.record.record as rec
import database.record.timerec as t
import airquality.database.util.query as qry
import airquality.looper.datelooper as looper

import airquality.adapter.api2db.measure as adapt
import airquality.adapter.db2api.param as par_adapt


class AtmotubeFetchSetup(setup.CommandSetup):

    def __init__(self, log_filename="atmotube"):
        super(AtmotubeFetchSetup, self).__init__(log_filename=log_filename)

    @log_decorator.log_decorator()
    def setup(self, sensor_type: str):
        # Load environment file
        fl.load_environment_file(file_path=comm_const.ENV_FILE_PATH, sensor_type=sensor_type)

        ################################ API-SIDE OBJECTS ################################
        # API parameters
        address, url_param = setup.get_api_parameters(sensor_type=sensor_type, log_filename=self.log_filename)

        # Check if 'format' argument is not missing from 'url_param'
        if 'format' not in url_param:
            raise SystemExit(f"{AtmotubeFetchSetup.__name__}: bad 'api.json' file structure => missing key='format'")

        # Take the API model format
        api_resp_fmt = url_param['format']

        # Setup API-side objects
        api_resp_parser = fp.get_text_parser(file_ext=api_resp_fmt, log_filename=self.log_filename)
        api_data_extractor = extr.AtmotubeSensorDataExtractor(log_filename=self.log_filename)
        url_builder = url.AtmotubeURL(address=address, url_param=url_param, log_filename=self.log_filename)

        # FetchWrapper
        fetch_wrapper = setup.get_fetch_wrapper(url_builder=url_builder,
                                                api_resp_parser=api_resp_parser,
                                                api_data_extractor=api_data_extractor,
                                                log_filename=self.log_filename)
        fetch_wrapper.set_file_logger(self.file_logger)
        fetch_wrapper.set_console_logger(self.console_logger)

        ################################ DATABASE-SIDE OBJECTS ################################
        # Database Connection
        database_connection = setup.open_database_connection(connection_string=os.environ['DBCONN'],
                                                             log_filename=self.log_filename)

        # Load SQL query file
        query_file_obj = setup.load_file(file_path=comm_const.QUERY_FILE_PATH, log_filename=self.log_filename)

        # QueryBuilder
        query_builder = qry.QueryBuilder(query_file=query_file_obj)

        # InsertWrapper
        insert_wrapper = ins.FetchMobileInsertWrapper(
            conn=database_connection,
            query_builder=query_builder,
            sensor_measure_rec=rec.MobileMeasureRecord(time_rec=t.TimeRecord(), location_rec=loc.LocationRecord()),
            log_filename=self.log_filename
        )
        insert_wrapper.set_file_logger(self.file_logger)
        insert_wrapper.set_console_logger(self.console_logger)

        # TypeSelectWrapper
        select_type_wrapper = sel_type.MobileTypeSelectWrapper(conn=database_connection,
                                                               query_builder=query_builder,
                                                               sensor_type=sensor_type)
        # SensorIDSelectWrapper
        sensor_id_select_wrapper = sel_type.SensorIDSelectWrapper(conn=database_connection,
                                                                  query_builder=query_builder,
                                                                  log_filename=self.log_filename)

        ################################ ADAPTER-SIDE OBJECTS ################################
        # Used for reshaping the sensor data into a proper shape for converting into SQL record
        api2db_adapter = adapt.AtmotubeMeasureAdapter(sel_type=select_type_wrapper)

        # Used for reshaping database api parameters for fetching data
        db2api_adapter = par_adapt.AtmotubeParamAdapter()

        # Date looper class
        date_looper_class = looper.get_date_looper_class(sensor_type=sensor_type)

        # Build command object
        cmd = command.FetchCommand(fetch_wrapper=fetch_wrapper,
                                   insert_wrapper=insert_wrapper,
                                   select_type_wrapper=select_type_wrapper,
                                   id_select_wrapper=sensor_id_select_wrapper,
                                   api2db_adapter=api2db_adapter,
                                   db2api_adapter=db2api_adapter,
                                   date_looper_class=date_looper_class)
        cmd.set_file_logger(self.file_logger)
        cmd.set_console_logger(self.console_logger)

        return cmd


class ThingspeakFetchSetup(setup.CommandSetup):

    def __init__(self, log_filename="atmotube"):
        super(ThingspeakFetchSetup, self).__init__(log_filename=log_filename)

    @log_decorator.log_decorator()
    def setup(self, sensor_type: str):
        # Load environment file
        fl.load_environment_file(file_path=comm_const.ENV_FILE_PATH, sensor_type=sensor_type)

        ################################ API-SIDE OBJECTS ################################
        # API parameters
        address, url_param = setup.get_api_parameters(sensor_type=sensor_type, log_filename=self.log_filename)

        # Check if 'format' argument is not missing from 'url_param'
        if 'format' not in url_param:
            raise SystemExit(f"{ThingspeakFetchSetup.__name__}: bad 'api.json' file structure => missing key='format'")

        # Take the API model format
        api_resp_fmt = url_param['format']

        # Setup API-side objects
        api_resp_parser = fp.get_text_parser(file_ext=api_resp_fmt, log_filename=self.log_filename)
        api_data_extractor = extr.ThingspeakAPIResponseModelBuilder(log_filename=self.log_filename)
        url_builder = url.ThingspeakURL(address=address, url_param=url_param, log_filename=self.log_filename)

        # FetchWrapper
        fetch_wrapper = setup.get_fetch_wrapper(url_builder=url_builder,
                                                api_resp_parser=api_resp_parser,
                                                api_data_extractor=api_data_extractor,
                                                log_filename=self.log_filename)
        fetch_wrapper.set_file_logger(self.file_logger)
        fetch_wrapper.set_console_logger(self.console_logger)

        ################################ DATABASE-SIDE OBJECTS ################################
        # Database Connection
        database_connection = setup.open_database_connection(connection_string=os.environ['DBCONN'],
                                                             log_filename=self.log_filename)

        # Load SQL query file
        query_file_obj = setup.load_file(file_path=comm_const.QUERY_FILE_PATH, log_filename=self.log_filename)

        # QueryBuilder
        query_builder = qry.QueryBuilder(query_file=query_file_obj)

        # InsertWrapper
        insert_wrapper = ins.FetchStationInsertWrapper(
            conn=database_connection,
            query_builder=query_builder,
            sensor_measure_rec=rec.StationMeasureRecord(time_rec=t.TimeRecord()),
            log_filename=self.log_filename
        )
        insert_wrapper.set_file_logger(self.file_logger)
        insert_wrapper.set_console_logger(self.console_logger)

        # TypeSelectWrapper
        select_type_wrapper = sel_type.StationTypeSelectWrapper(conn=database_connection,
                                                                query_builder=query_builder,
                                                                sensor_type=sensor_type)
        # SensorIDSelectWrapper
        sensor_id_select_wrapper = sel_type.SensorIDSelectWrapper(conn=database_connection,
                                                                  query_builder=query_builder,
                                                                  log_filename=self.log_filename)

        ################################ ADAPTER-SIDE OBJECTS ################################
        # Used for reshaping the sensor data into a proper shape for converting into SQL record
        api2db_adapter = adapt.ThingspeakMeasureAdapter(sel_type=select_type_wrapper)

        # Used for reshaping database api parameters for fetching data
        db2api_adapter = par_adapt.ThingspeakParamAdapter()

        # Date looper class
        date_looper_class = looper.get_date_looper_class(sensor_type=sensor_type)

        # Build command object
        cmd = command.FetchCommand(fetch_wrapper=fetch_wrapper,
                                   insert_wrapper=insert_wrapper,
                                   select_type_wrapper=select_type_wrapper,
                                   id_select_wrapper=sensor_id_select_wrapper,
                                   api2db_adapter=api2db_adapter,
                                   db2api_adapter=db2api_adapter,
                                   date_looper_class=date_looper_class)
        cmd.set_file_logger(self.file_logger)
        cmd.set_console_logger(self.console_logger)

        return cmd
