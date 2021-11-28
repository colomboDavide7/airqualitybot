######################################################
#
# Author: Davide Colombo
# Date: 28/11/21 15:23
# Description: INSERT HERE THE DESCRIPTION
#
######################################################
import airquality.database.conn.adapt as conn


def get_database_adapter(connection_string: str, adapter_type="psycopg2", log_filename="log"):

    if adapter_type == 'psycopg2':
        return conn.Psycopg2DatabaseAdapter(connection_string=connection_string, log_filename=log_filename)
    else:
        raise SystemExit(f"'{get_database_adapter.__name__}():' bad adapter type '{adapter_type}'")
