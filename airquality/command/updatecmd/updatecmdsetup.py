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

import airquality.api.fetchwrp as apiwrp
import airquality.api.url.purpurl as url
import airquality.api.resp.purpresp as resp

import airquality.api2db.purpadpt as padpt

import airquality.database.op.ins.stgeoins as ins
import airquality.database.op.sel.stationsel as sel
import airquality.database.util.query as qry


class PurpleairUpdateSetup(setup.CommandSetup):

    def __init__(self, log_filename="log"):
        super(PurpleairUpdateSetup, self).__init__(log_filename=log_filename)

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

        # Load SQL query file
        query_file_obj = setup.load_file(file_path=comm_const.QUERY_FILE_PATH, log_filename=self.log_filename)
        query_builder = qry.QueryBuilder(query_file=query_file_obj)

        # InsertWrapper
        insert_wrapper = ins.StationGeoInsertWrapper(conn=database_conn, builder=query_builder, log_filename=self.log_filename)
        insert_wrapper.set_file_logger(self.file_logger)
        insert_wrapper.set_console_logger(self.console_logger)

        # SelectWrapper
        select_wrapper = sel.StationSelectWrapper(
            conn=database_conn,
            builder=query_builder,
            sensor_type=sensor_type,
            log_filename=self.log_filename
        )

        ################################ COMMAND OBJECT ################################
        cmd = command.UpdateCommand(
            ara=padpt.PurpAPIRespAdpt(),
            ub=url_builder,
            fw=fetch_wrapper,
            iw=insert_wrapper,
            sw=select_wrapper,
            log_filename=self.log_filename
        )
        cmd.set_file_logger(self.file_logger)
        cmd.set_console_logger(self.console_logger)

        return cmd
