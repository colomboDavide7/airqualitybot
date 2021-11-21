######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 16:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import airquality.command.update.purpleair as command
import airquality.command.config as comm_const
import airquality.command.setup as setup

import airquality.logger.util.decorator as log_decorator

import airquality.file.util.parser as fp
import airquality.file.util.loader as fl

import airquality.api.util.extractor as extr
import airquality.api.util.url as url

import airquality.database.operation.select.type as sel_type
import airquality.database.util.datatype.timestamp as ts
import airquality.database.util.record.location as loc
import airquality.database.operation.insert.update as ins
import airquality.database.util.postgis.geom as geom
import airquality.database.util.record.record as rec
import airquality.database.util.record.time as t
import airquality.database.util.query as qry

import airquality.adapter.api2db.sensor as adapt


class PurpleairUpdateSetup(setup.CommandSetup):

    def __init__(self, log_filename="log"):
        super(PurpleairUpdateSetup, self).__init__(log_filename=log_filename)

    @log_decorator.log_decorator()
    def setup(self, sensor_type: str):
        # Load environment file
        fl.load_environment_file(file_path=comm_const.ENV_FILE_PATH, sensor_type=sensor_type)

        ################################ API-SIDE OBJECTS ################################
        # Load API file
        api_file_obj = setup.load_file(file_path=comm_const.API_FILE_PATH,
                                       path_to_object=[sensor_type],
                                       log_filename=self.log_filename)
        # Get API address
        address = api_file_obj.api_address

        # Get URL param
        url_param = api_file_obj.url_param
        url_param.update({'api_key': os.environ['PURPLEAIR_KEY1']})

        # Setup API-side objects
        api_resp_parser = fp.JSONParser(log_filename=self.log_filename)
        api_data_extractor = extr.PurpleairDataExtractor(log_filename=self.log_filename)
        url_builder = url.PurpleairURL(address=address, url_param=url_param, log_filename=self.log_filename)

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
        insert_wrapper = ins.UpdateInsertWrapper(
            conn=database_connection,
            query_builder=query_builder,
            sensor_location_rec=rec.SensorLocationRecord(time_rec=t.TimeRecord(), location_rec=loc.LocationRecord()),
            log_filename=self.log_filename
        )
        insert_wrapper.set_file_logger(self.file_logger)
        insert_wrapper.set_console_logger(self.console_logger)

        # TypeSelectWrapper
        select_type_wrapper = sel_type.StationTypeSelectWrapper(conn=database_connection,
                                                                query_builder=query_builder,
                                                                sensor_type=sensor_type)
        ################################ ADAPTER-SIDE OBJECTS ################################
        api2db_adapter = adapt.PurpleairSensorAdapter(
            postgis_class=geom.PointBuilder,
            timestamp_class=ts.UnixTimestamp,
            log_filename=self.log_filename
        )

        # Build command object
        cmd = command.PurpleairUpdateCommand(fetch_wrapper=fetch_wrapper,
                                             insert_wrapper=insert_wrapper,
                                             select_type_wrapper=select_type_wrapper,
                                             api2db_adapter=api2db_adapter)
        cmd.set_file_logger(self.file_logger)
        cmd.set_console_logger(self.console_logger)

        return cmd
