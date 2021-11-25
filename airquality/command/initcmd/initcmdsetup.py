######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 11:13
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import airquality.command.initcmd.initcmd as command
import airquality.command.cmdconf as comm_const
import airquality.command.basecmdsetup as setup

import airquality.logger.util.decorator as log_decorator

import airquality.file.util.parser as fp
import airquality.file.util.loader as fl

import airquality.api.resp.purpresp as resp
import airquality.api.url.purpurl as url
import airquality.api.fetchwrp as apiwrp
import airquality.api2db.purpadpt as padpt

import airquality.database.op.ins.stinfoins as ins
import airquality.database.op.sel.stationsel as sel
import airquality.database.ext.postgis as postgis
import airquality.database.util.query as qry


################################ PURPLEAIR INIT COMMAND SETUP ################################
class PurpleairInitSetup(setup.CommandSetup):

    def __init__(self, log_filename="purpleair"):
        super(PurpleairInitSetup, self).__init__(log_filename=log_filename)

    @log_decorator.log_decorator()
    def setup(self, sensor_type: str):
        # Load environment file
        fl.load_environment_file(file_path=comm_const.ENV_FILE_PATH, sensor_type=sensor_type)

        ################################ API-SIDE OBJECTS ################################
        # API parameters
        api_file_obj = setup.load_file(
            file_path=comm_const.API_FILE_PATH, path_to_object=[sensor_type], log_filename=self.log_filename
        )

        # API parameters from file
        address = api_file_obj.address
        fields = api_file_obj.fields
        options = api_file_obj.options
        bounding_box = api_file_obj.bounding_box

        # URL Builder
        url_builder = url.PurpleairURLBuilder(
            address=address, fields=fields, key=os.environ['PURPLEAIR_KEY1'], bounding_box=bounding_box, options=options
        )

        # FetchWrapper
        fetch_wrapper = apiwrp.FetchWrapper(
            resp_builder=resp.PurpAPIRespBuilder(),
            resp_parser=fp.JSONParser(log_filename=self.log_filename),
            log_filename=self.log_filename
        )
        fetch_wrapper.set_file_logger(self.file_logger)
        fetch_wrapper.set_console_logger(self.console_logger)

        ################################ DATABASE-SIDE OBJECTS ################################
        # Database Connection
        database_conn = setup.open_database_connection(connection_string=os.environ['DBCONN'], log_filename=self.log_filename)

        # Load query file
        query_file_obj = setup.load_file(file_path=comm_const.QUERY_FILE_PATH, log_filename=self.log_filename)
        query_builder = qry.QueryBuilder(query_file=query_file_obj)

        # Station Info Insert Wrapper
        insert_wrapper = ins.StationInfoInsertWrapper(conn=database_conn, builder=query_builder, log_filename=self.log_filename)
        insert_wrapper.set_file_logger(self.file_logger)
        insert_wrapper.set_console_logger(self.console_logger)

        # SelectWrapper
        select_wrapper = sel.StationSelectWrapper(
            conn=database_conn,
            builder=query_builder,
            postgis_class=postgis.PostgisPoint,
            sensor_type=sensor_type,
            log_filename=self.log_filename
        )
        select_wrapper.set_file_logger(self.file_logger)
        select_wrapper.set_console_logger(self.console_logger)

        ################################ COMMAND OBJECT ################################
        cmd = command.InitCommand(
            ara=padpt.PurpAPIRespAdpt(),            # for adapt for reshaping api responses
            ub=url_builder,                         # for building api url for fetching sensor data from api
            fw=fetch_wrapper,                       # for fetching api sensor data
            iw=insert_wrapper,                      # for inserting sensor data fetched from api
            sw=select_wrapper,                      # for selecting sensor data from the database
            log_filename=self.log_filename          # name of the logging file used by the log decorator
        )
        cmd.set_file_logger(self.file_logger)
        cmd.set_console_logger(self.console_logger)

        return cmd
