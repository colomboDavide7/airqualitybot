######################################################
#
# Author: Davide Colombo
# Date: 25/11/21 20:26
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import os
import airquality.command.fetchcmd.fetchcmd as command
import airquality.command.cmdconf as comm_const
import airquality.command.basecmdsetup as setup

import airquality.logger.util.decorator as log_decorator

import airquality.file.util.parser as fp
import airquality.file.util.loader as fl

import airquality.api.fetchwrp as apiwrp
import airquality.api.url.atmurl as atmurl
import airquality.api.resp.atmresp as atmresp

import airquality.database.op.ins.mbmeasins as ins
import airquality.database.op.sel.mobilesel as sel

import airquality.database.util.query as qry


class AtmotubeFetchSetup(setup.CommandSetup):

    def __init__(self, log_filename="atmotube"):
        super(AtmotubeFetchSetup, self).__init__(log_filename=log_filename)

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
        options = api_file_obj.options

        url_builder = atmurl.AtmotubeURLBuilder(address=address, options=options)

        # FetchWrapper
        fetch_wrapper = apiwrp.FetchWrapper(
            resp_builder=atmresp.AtmoAPIRespBuilder(),
            resp_parser=fp.get_text_parser(file_ext=options.get('format'), log_filename=self.log_filename),
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
        insert_wrapper = ins.MobileMeasureInsertWrapper(conn=database_conn, builder=query_builder, log_filename=self.log_filename)
        insert_wrapper.set_file_logger(self.file_logger)
        insert_wrapper.set_console_logger(self.console_logger)

        # TypeSelectWrapper
        select_wrapper = sel.MobileSelectWrapper(
            conn=database_conn,
            builder=query_builder,
            sensor_type=sensor_type,
            log_filename=self.log_filename
        )

        # Build command object
        cmd = command.FetchCommand()
        cmd.set_file_logger(self.file_logger)
        cmd.set_console_logger(self.console_logger)
        return cmd
