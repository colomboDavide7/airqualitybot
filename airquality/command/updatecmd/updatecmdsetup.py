######################################################
#
# Author: Davide Colombo
# Date: 21/11/21 16:41
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import airquality.command.updatecmd.updatecmd as command
import airquality.command.cmdconf as comm_const
import airquality.command.basecmdsetup as setup

import airquality.logger.util.decorator as log_decorator

import airquality.file.util.parser as fp
import airquality.file.util.loader as fl

import airquality.api.url.purpurl as url
import airquality.api.resp.purpresp as resp

import airquality.api2db.updtunif.updtunif as unif

import airquality.database.op.ins.updtins as ins
import airquality.database.op.sel.stationsel as sel
import airquality.database.util.query as qry
import airquality.database.rec.updtrec as rec


class PurpleairUpdateSetup(setup.CommandSetup):

    def __init__(self, log_filename="log"):
        super(PurpleairUpdateSetup, self).__init__(log_filename=log_filename)

    @log_decorator.log_decorator()
    def setup(self, sensor_type: str):
        # Load environment file
        fl.load_environment_file(file_path=comm_const.ENV_FILE_PATH, sensor_type=sensor_type)

        ################################ API-SIDE OBJECTS ################################
        # API parameters
        address, url_param = setup.get_api_parameters(sensor_type=sensor_type, log_filename=self.log_filename)
        url_param.update({'api_key': os.environ['PURPLEAIR_KEY1']})

        # Setup API-side objects
        response_parser = fp.JSONParser(log_filename=self.log_filename)
        response_builder = resp.PurpleairAPIResponseBuilder()
        url_builder = url.PurpleairURL(address=address, parameters=url_param, log_filename=self.log_filename)

        # FetchWrapper
        fetch_wrapper = setup.get_fetch_wrapper(url_builder=url_builder,
                                                response_parser=response_parser,
                                                response_builder=response_builder,
                                                log_filename=self.log_filename)
        fetch_wrapper.set_file_logger(self.file_logger)
        fetch_wrapper.set_console_logger(self.console_logger)

        ################################ DATABASE-SIDE OBJECTS ################################
        # Database Connection
        database_connection = setup.open_database_connection(connection_string=os.environ['DBCONN'], log_filename=self.log_filename)

        # Load SQL query file
        query_file_obj = setup.load_file(file_path=comm_const.QUERY_FILE_PATH, log_filename=self.log_filename)

        # QueryBuilder
        query_builder = qry.QueryBuilder(query_file=query_file_obj)

        # InsertWrapper
        insert_wrapper = ins.UpdateInsertWrapper(conn=database_connection,
                                                 query_builder=query_builder,
                                                 log_filename=self.log_filename)
        insert_wrapper.set_file_logger(self.file_logger)
        insert_wrapper.set_console_logger(self.console_logger)

        # SelectWrapper
        select_wrapper = sel.StationSelectWrapper(
            conn=database_connection,
            query_builder=query_builder,
            sensor_type=sensor_type,
            log_filename=self.log_filename
        )

        ################################ COMMAND OBJECT ################################
        cmd = command.UpdateCommand(
            fw=fetch_wrapper,
            iw=insert_wrapper,
            sw=select_wrapper,
            urb=unif.UpdateUniformResponseBuilder(),
            rb=rec.UpdateRecordBuilder(),
            log_filename=self.log_filename
        )
        cmd.set_file_logger(self.file_logger)
        cmd.set_console_logger(self.console_logger)

        return cmd
